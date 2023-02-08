from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
import csv


from genomeBact.models import Genome,Transcript
from genomeBact.forms import GenomeForm, TranscriptForm, UploadFileForm, CreateUserForm
from Bio import SeqIO
from io import StringIO

from .models import Genome,Transcript
from .forms import GenomeForm, TranscriptForm, CreateUserForm
from .decorators import unauthenticated_user, allowed_users, admin_only

from scripts.utils import get_max_length

def user_logout(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def user_login(request):

    request.session.clear()
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password') 

        user = authenticate(request, username= username, password= password )

        if user is not None:
            login(request, user)
            return redirect('home')
        else:   
            messages.info(request, "Username or password is incorrect" )

    context = {}
    return render(request, 'genomeBact/login.html', context)

@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)  
        if form.is_valid():
            user = form.save()

            group = request.POST.get('group')
            group = Group.objects.get(name = group)
            user.groups.add(group)

            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            
            return redirect('login')
    else:
        form = CreateUserForm()

    context = {'form':form}
    return render(request, 'genomeBact/register.html', context)

@login_required(login_url='login')
def home(request):

    

    # Does user submit anything ?
    if request.method == "POST":    
      
        # User submits but don't fill any research field
        if request.POST.keys() is not None:

            # Genome or transcript ?
            query_type = request.POST.get("query_type")
            request.session["query_type"] = query_type

            if query_type == "Genome":

                request.session["accession"] = request.POST.get("accession", "")
                request.session["specie"] = request.POST.get("specie", "")
                request.session["max"] = request.POST.get("max_length")
                request.session["min"] = request.POST.get("min_length")

                if request.POST.get("sub_nt"):

                    # Minimum substring length to search
                    if len(request.POST.get("sub_nt")) < 3:

                        request.session["sub_nt"] = ""
                    
                    else:

                        request.session["sub_nt"] = request.POST.get("sub_nt")
                else:

                    request.session["sub_nt"] = ""

                return redirect("results")

            if query_type == "Transcript":

                accession= request.POST.get("accession", "")
                specie = request.POST.get("specie", "")

                default_max = get_max_length()
                max_ = request.POST.get("max_length", default_max)
                min_ = request.POST.get("min_length", 0)

                if request.POST.get("sub_nt"):

                    # Minimum substring length to search
                    if len(request.POST.get("sub_nt")) < 3:

                        sub_nt = ""
                    
                    else:

                        sub_nt = request.POST.get("sub_nt")
                else:

                    sub_nt = ""


                if request.POST.get("sub_pep"):

                    # Minimum substring length to search
                    if len(request.POST.get("sub_pep")) < 3:

                        sub_pep = ""
                    
                    else:

                        sub_pep = request.POST.get("sub_pep")
                else:

                    sub_pep = ""

                if ( not request.POST.get("specie") ) or request.POST.get("specie") == "":

                    query_max = Q(length__gte = min_)
                    query_min = Q(length__lte = max_)
                    query_access = Q(chromosome__contains = accession)
                    query_sub_nt = Q(seq_nt__contains = sub_nt)
                    query_sub_pep = Q(seq_cds__contains = sub_pep)
                    query_specie = Q(specie__contains = specie)

                    Transcripts = Transcript.objects.filter(query_max & query_min & query_access & query_sub_nt & query_sub_pep)

                    # Pour plus tard : transcripts = Transcript.objects.filter(chromosome__in = genomes)
                    # retourne les trancripts des ( )


                return render(request, "genomeBact/transcript_list.html",{'genome': genome, 'transcript': transcript})

    # Return empty research fields to results/ if user don't submit button
    request.session["accession"] = ""
    request.session["specie"] = ""
    request.session["max"] = ""
    request.session["min"] = ""
    request.session["substring"] = ""
    request.session["query_type"] = ""

    return render(request,'genomeBact/home.html')

def download_csv(request, transcripts = None, genomes = None):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transcripts.csv"'

    writer = csv.writer(response)
    writer.writerow(['Accession', 'Sequence'])

    if transcripts:

        for transcript in transcripts:
            writer.writerow([transcript.transcript, transcript.seq_cds])

        return response

    elif genomes:

        for genome in genomes:

            writer.writerow([genome.chromosome, genome.sequence])
        return response


@login_required(login_url='login')
@allowed_users(allowed_roles=['Lecteur'])
# If user don't search anything from home page, return full list of genomes
def results(request):

    
    # Delete session without deleting user current logs
    keys = ["accession","specie","sub_nt","sub_pep", "max","min", "query_type"]
    keys = [key for key in keys if key in request.session.keys() ]

    
    accession = request.session["accession"] 
    specie = request.session["specie"]
    substring = request.session["substring"]
    substring = substring.upper() # Just in case

    # For some reason request.session doesn't store request.POST.get(name, default_integer) default output as integer but rather as ''
    max_ = request.session["max"]
    if max_ == '':
        max_ = get_max_length()
    min_ = request.session["min"]
    if min_ == '':
        min_ = 0

    query_max = Q(length__gte = min_)
    query_min = Q(length__lte = max_)
    query_access = Q(chromosome__contains = accession)
    query_sub = Q(sequence__contains = substring)
    query_specie = Q(specie__contains = specie)

    genomes = Genome.objects.filter(query_max & query_min & query_access & query_sub & query_specie)

    #for key in keys:
    #    del request.session[key]

        
    if request.method == 'POST':


        if not genomes:

            return render(request, '404.html', status=404)

        else:

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="models.csv"'

            writer = csv.writer(response)
            writer.writerow(['Number', 'Text'])

        
            for genome in genomes:
                writer.writerow([genome.chromosome, genome.specie])

            return response
        
    return render(request,'genomeBact/results.html', {'genomes': genomes}) 


       


@login_required(login_url='login')
def genome_detail(request, specie):
    genome = Genome.objects.get(specie=specie)
    transcript = Transcript.objects.filter(chromosome = genome.chromosome)

    sequence = genome.sequence



    return render(request,'genomeBact/genome_detail.html',{'genome': genome, 'transcript': transcript})

@login_required(login_url='login')
def transcript_list(request, specie):


    
    genome = Genome.objects.get(specie=specie)
    transcript = Transcript.objects.filter(chromosome = genome.chromosome)

    return render(request, 'genomeBact/transcript_list.html',{'genome': genome, 'transcript': transcript})











@login_required(login_url='login')
def transcript_create(request, specie):
    genome = Genome.objects.get(specie=specie)

    if request.method == 'POST':
        form = TranscriptForm(request.POST)  
        if form.is_valid():
            form.instance.chromosome = genome
            form.save()
            #return redirect('transcript-list', genome.specie)
            return redirect('genome-detail', genome.specie)
    else:
        form = TranscriptForm()

    return render(request,'genomeBact/transcript_create.html',{'form': form, 'genome' : genome}) 

@login_required(login_url='login')
def transcript_detail(request, specie, transcript):

    genome = Genome.objects.get(specie=specie)
    transcript = Transcript.objects.get(transcript=transcript)
    
    return render(request,'genomeBact/transcript_detail.html',{'genome':genome,'transcript': transcript})

@login_required(login_url='login')
def transcript_annot(request, transcript):
    transcript = Transcript.objects.get(transcript=transcript)

    return render(request,'genomeBact/transcript_annot.html',{'transcript': transcript})

@login_required(login_url='login')
@admin_only
def admin(request):

    return render(request,'genomeBact/admin.html')

@login_required(login_url='login')
def settings(request):
    
    return render(request,'genomeBact/user_settings.html')

@login_required(login_url='login')
def validator(request):
    
    return render(request,'genomeBact/validator.html')

@login_required(login_url='login')
def assign_transcript(request):
    
    return render(request,'genomeBact/assign_transcript.html')

@login_required(login_url='login')
def transcript_list_state(request):
    
    return render(request,'genomeBact/transcript_list_state.html')

@login_required(login_url='login')
def transcript_to_validate(request):
    
    return render(request,'genomeBact/transcript_to_validate.html')

@login_required(login_url='login')
def annotator(request):
    
    return render(request,'genomeBact/annotator.html')

@login_required(login_url='login')
def transcript_to_annot(request):
    
    return render(request,'genomeBact/transcript_to_annot.html')


### NOT CURRENTLY WORKING NEED TO ADD GENOME FOR WHICH TRANSCRIPTS ARE UPLOADED ###
def transcript_upload(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid() :
            
            file = request.FILES['file'] # Returns HttpRequest object

            # Convert byte to text mode for BioPython SeqIO
            stringio = StringIO(file.read().decode("utf-8")) 
            for record in SeqIO.parse(stringio, 'fasta'):
                t = Transcript(sequence = record.description)
                t.save()
            
     
        return HttpResponse(" Chargement réussi ! ")
    else:
        form = UploadFileForm()

    return render(request, 'polls/transcript_upload.html', {'form': form})