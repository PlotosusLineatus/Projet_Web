from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from genomeBact.models import Genome,Transcript
from genomeBact.forms import GenomeForm, TranscriptForm, CreateUserForm

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else : 
        if request.method == 'POST':
            username = request.POST.get('username') 
            password = request.POST.get('password') 

            user = authenticate(request, username= username, password= password )

            if user is not None:
                login(request, user)
                return redirect('home')
            else:   
                messages.info(request, "Username or password is incorrect" )
            #return render(request, 'genomeBact/login.html', context)

        context = {}
        return render(request, 'genomeBact/login.html', context)

def user_logout(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)  
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user )
                return redirect('login')
        else:
            form = CreateUserForm()

        context = {'form':form}
        return render(request, 'genomeBact/register.html', context)

@login_required(login_url='login')
def home(request):
    ## Pour ajouter des génomes (mais c'est pour nous ça) ##
        if request.method == 'POST':
            form = GenomeForm(request.POST)  
            if form.is_valid():
                new_genome = form.save()
                return redirect('genome-detail', new_genome.specie)
        else:
            form = GenomeForm()

        return render(request,'genomeBact/home.html',{'form': form})
    #return render(request, 'genomeBact/home.html')

@login_required(login_url='login')
def results(request):
    genome = Genome.objects.all()
    return render(request, 'genomeBact/results.html',{'genome': genome})

@login_required(login_url='login')
def genome_detail(request, specie):
    genome = Genome.objects.get(specie=specie)

    return render(request,'genomeBact/genome_detail.html',{'genome': genome})

@login_required(login_url='login')
def transcript_list(request, specie):
    genome = Genome.objects.get(specie=specie)
    transcript = Transcript.objects.filter(chromosome = genome.id)

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

    
