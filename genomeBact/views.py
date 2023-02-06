from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db.models.functions import Now
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse


from Bio import SeqIO
from io import StringIO

from .models import Genome,Transcript,Profile, Connexion
from .forms import GenomeForm, TranscriptForm, UploadFileForm, CreateUserForm, AnnotForm
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
            Connexion.objects.create(user = user, date=Now())
            return redirect('home')
        else :
            try:
                username = User.objects.get(email=username)
                user = authenticate(request, username= username.username, password= password )
                login(request, user)
                Connexion.objects.create(user = user, date=Now())
                return redirect('home')           
            except User.DoesNotExist:
                messages.info(request, "Username or password is incorrect" )
            

    context = {}
    return render(request, 'genomeBact/login.html', context)

@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)  
        if form.is_valid() and request.POST.get('email')!= None:
            user = form.save()

            group = request.POST.get('group')
            group = Group.objects.get(name = group)
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            
            Profile.objects.create(user = user, name=user.username)

            messages.success(request, 'Account was created for ' + username)
            
            return redirect('login')
        else:
            messages.error(request, form.errors)
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
def results(request):
    # If user don't search anything from home page, return full list of genomes
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
@allowed_users(allowed_roles=['Admin','Validateur'])
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
    cds = Transcript.objects.get(transcript=transcript)

    if request.method == 'POST':
        form = AnnotForm(request.POST)  

        if 'Validate' in request.POST:
            Transcript.objects.filter(transcript=transcript).update(status = 'validated', status_date = Now(), annotator=None)
            messages.success(request, 'Annotations were validated.')
            return HttpResponseRedirect(request.path_info)
        elif 'to_validate' in request.POST:
            Transcript.objects.filter(transcript=transcript).update(status = 'annotated', status_date = Now())
            messages.success(request, 'Annotations were send for validation.')
            return HttpResponseRedirect(request.path_info)
        elif 'reject_validation' in request.POST:
            Transcript.objects.filter(transcript=transcript).update(status = 'assigned', status_date = Now())
            messages.success(request, 'Annotations were send back to '+ cds.annotator.name )
            return HttpResponseRedirect(request.path_info)
        elif form.is_valid():
            annotations = form.save(commit=False)
            gene = annotations.gene
            gene_biotype = annotations.gene_biotype
            transcript_biotype = annotations.transcript_biotype
            gene_symbol = annotations.gene_symbol
            description = annotations.description

            Transcript.objects.filter(transcript=transcript).update(gene = gene, gene_biotype=gene_biotype, transcript_biotype=transcript_biotype, gene_symbol=gene_symbol, description=description, status_date = Now())
            
            messages.success(request, 'Annotations were saved.')
            
            return HttpResponseRedirect(request.path_info)
    else:
        form = AnnotForm()

    context = {'genome':genome,'transcript': cds, 'form':form}
    return render(request, 'genomeBact/transcript_detail.html', context)
    
@login_required(login_url='login')
def transcript_annot(request, transcript):
    transcript = Transcript.objects.get(transcript=transcript)

    return render(request,'genomeBact/transcript_annot.html',{'transcript': transcript})

@login_required(login_url='login')
@admin_only
def admin(request):

    return render(request,'genomeBact/admin.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Validateur','Annotateur'])
def workspace(request):
    transcripts_to_annotate = request.user.profile.to_annotate.all()
    #transcripts_to_annotate = request.user.profile.transcript_set.all()
    transcripts_to_assign = Transcript.objects.filter(status = 'empty')
    transcripts_to_validate = Transcript.objects.filter(status = 'annotated')
    annotators = User.objects.filter(groups__name='Annotateur')

    if request.method == 'POST':
        annotator_chosen = request.POST.get('annotator')
        transcript_chosen = request.POST.get('transcript_annot')
        
        if( request.user.groups.all()[0].name == 'Validateur'):
            ### ASSIGNING A TRANSCRIPT
            if annotator_chosen != None and transcript_chosen!= None:
                    
                #transcript_chosen = Transcript.objects.get(transcript=transcript_chosen)
                
                Transcript.objects.filter(transcript=transcript_chosen).update(annotator = Profile.objects.get(name=annotator_chosen))
                Transcript.objects.filter(transcript=transcript_chosen).update(validator = Profile.objects.get(name=request.user.username))
                Transcript.objects.filter(transcript=transcript_chosen).update(status = 'assigned')
                
                messages.success(request, transcript_chosen +' was assigned for ' + annotator_chosen + ".")

            else:
                messages.info(request, " Please select an Annotator AND a Transcript" )


    context = {'transcripts_to_annotate':transcripts_to_annotate, 'transcripts_to_assign':transcripts_to_assign, 'annotators':annotators,'transcripts_to_validate':transcripts_to_validate}
    return render(request,'genomeBact/workspace.html', context)

@login_required(login_url='login')
def settings(request):
    all_con = request.user.connexion_set.all()

    context = {'connexions': all_con}
    return render(request, 'genomeBact/user_settings.html', context)



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
@login_required(login_url='login')
@admin_only
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