from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse


from genomeBact.models import Genome,Transcript, Profile
from genomeBact.forms import GenomeForm, TranscriptForm, UploadFileForm, CreateUserForm
from Bio import SeqIO
from io import StringIO

from .models import Genome,Transcript
from .forms import GenomeForm, TranscriptForm, CreateUserForm
from .decorators import unauthenticated_user, allowed_users, admin_only

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
            
            Profile.objects.create(user = user, name=user.username)

            messages.success(request, 'Account was created for ' + username)
            
            return redirect('login')
    else:
        form = CreateUserForm()

    context = {'form':form}
    return render(request, 'genomeBact/register.html', context)

@login_required(login_url='login')
def home(request):

   
    if request.method == "POST":    

        user_input = request.POST.get('accession', None)

        # On regarde si le code d'accession contient quelque chose
        if user_input is not None:
            query_type = request.POST.get("query_type", None)

            # Si l'utilisateur a sélectionné " Genome " ( au lieu de " Transcript ")
            if query_type == "Genome":
                request.session['user_input'] = user_input ## j'enregistre dans les cookies {'user_input' = user_input}
                # Je veux retourner sur la page results en renvoyant ce que l'utilisateur a entré pour sa recherche
                return redirect( 'results')

    return render(request,'genomeBact/home.html')



@login_required(login_url='login')
@allowed_users(allowed_roles=['Lecteur'])
# If user don't search anything from home page, return full list of genomes
def results(request):
    if 'user_input' in request.session:
        user_input = request.session['user_input'] ## je récupère la variable dans les cookies
        del request.session['user_input'] ## Je supprime les cookies car on en a plus besoin
        # Sinon, on utilise l'input de l'user pour filtrer les génomes sur leur num d'accession
        genome = Genome.objects.filter(chromosome__contains = user_input)
        return render(request, 'genomeBact/results.html',{'genome': genome}) 

    else:
        # On accède à la page normalement si l'input de l'user est inexistant  
        genome = Genome.objects.all()
        return render(request, 'genomeBact/results.html',{'genome': genome}) 

       


@login_required(login_url='login')
def genome_detail(request, specie):
    genome = Genome.objects.get(specie=specie)
    transcripts = Transcript.objects.filter(chromosome = genome.chromosome)

    sequence = genome.sequence

    return render(request,'genomeBact/genome_detail.html',{'genome': genome, 'transcripts' : transcripts})
    
@login_required(login_url='login')
def transcript_list(request, specie):
    genome = Genome.objects.get(specie=specie)
    transcripts = Transcript.objects.filter(chromosome = genome.chromosome)

    return render(request, 'genomeBact/transcript_list.html',{'genome': genome, 'transcripts': transcripts})

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
    transcripts = request.user.profile.transcript_set.all()
    print('____________TRANSCRIPTS: ', transcripts)
    #AAC73112

    if request.method == 'POST':
        print("\n ___________POST   \n")
        annotator = request.POST.get('annotator')
        transcript_annot = request.POST.get('transcript_annot')
        
        if annotator != None and transcript_annot!= None:
            '''
            if (Transcript.objects.get(transcript=transcript_annot).DoesNotExist() 
                    and Profile.objects.get(name=annotator).DoesNotExist()):
                messages.info(request, " Please enter a VALID User and Transcript" )  
             
            else:
            '''
            transcript = Transcript.objects.get(transcript=transcript_annot)
            annotator = Profile.objects.get(name=annotator)
            print(annotator.name)
            print(transcript.transcript)

            Transcript.objects.filter(transcript=transcript_annot).update(annotator = annotator)
            Transcript.objects.filter(transcript=transcript_annot).update(status = 'assigned')
            
            print("\n   ---"+transcript.status + " "+ annotator.name +"    ---    \n")
            messages.success(request, transcript_annot +' was assigned for ' + annotator.name)
            #return redirect('home')

        else:
            messages.info(request, " Please enter a User AND a Transcript" )

    context = {'transcripts':transcripts}
    return render(request,'genomeBact/user_settings.html', context)

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