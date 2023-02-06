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

    if request.method == "POST":    
      
    
        # On regarde si le code d'accession contient quelque chose
        if request.POST.keys() is not None:

            query_type = request.POST.get("query_type")

            # Si l'utilisateur a sélectionné " Genome " ( au lieu de " Transcript ")
            if query_type == "Genome":

                request.session["accession"] = request.POST.get("accession", "")
                request.session["specie"] = request.POST.get("specie", "")

                if request.POST.get("substring") is not None:
                    if len(request.POST.get("substring")) < 3:
                        request.session["substring"] = ""
                    
                    else:
                        request.session["substring"] = request.POST.get("substring")
                else:
                    request.session["substring"] = request.POST.get("substring")

                max_length = request.POST.get("max_length")
                request.session["max_length"] = int(max_length) if max_length.strip() else 0
                min_length = request.POST.get("min_length")
                request.session["min_length"] = int(min_length) if min_length.strip() else 0



                return HttpResponseRedirect("results")

            if query_type == "Transcript":

                request.sesion["accession"] = request.POST.get("accession", "")

                return redirect("transcript_detail")

    return render(request,'genomeBact/home.html')

def download_transcripts(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transcripts.csv"'

    writer = csv.writer(response)
    writer.writerow(['Accession', 'Sequence'])

    transcripts = Transcript.objects.all()
    for transcript in transcripts:
        writer.writerow([transcript.transcript, transcript.seq_cds])

    return response


@login_required(login_url='login')
@allowed_users(allowed_roles=['Lecteur'])
# If user don't search anything from home page, return full list of genomes
def results(request):

    keys = ["accession","specie","max_length","min_length","substring"]

    if ("accession" or "specie" or "max_length" or "min_length" or "substring") in request.session.keys():

        accession = request.session["accession"] ## je récupère la variable dans les cookies
        specie = request.session["specie"]
        max_length = request.session["max_length"]
        min_length = request.session["min_length"]
        substring = request.session["substring"]
        substring = substring.upper()

        genome = Genome.objects.filter(Q(specie__contains = specie) & Q(sequence__contains = substring) & Q(chromosome__contains = accession) & Q(length__gte =min_length) & Q(length_lte = max_length))


        for key in keys:
            del request.session[key] ## Je supprime les cookies car on en a plus besoin

        return render(request, 'genomeBact/results.html',{'genome': genome}) 

    else:
        # On accède à la page normalement si l'input de l'user est inexistant  
        genome = Genome.objects.all()
        return render(request, 'genomeBact/results.html',{'genome': genome}) 

       


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