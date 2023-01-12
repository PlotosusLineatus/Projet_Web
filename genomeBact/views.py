from django.shortcuts import redirect, render
from genomeBact.models import Genome,Transcript
from genomeBact.forms import GenomeForm, TranscriptForm

def login(request):
    
    return render(request, 'genomeBact/login.html')

def register(request):
    
    return render(request, 'genomeBact/register.html')

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

def results(request):
    genome = Genome.objects.all()
    return render(request, 'genomeBact/results.html',{'genome': genome})

def genome_detail(request, specie):
    genome = Genome.objects.get(specie=specie)

    return render(request,'genomeBact/genome_detail.html',{'genome': genome})

def transcript_list(request, specie):
    genome = Genome.objects.get(specie=specie)
    transcript = Transcript.objects.filter(chromosome = genome.chromosome)

    return render(request, 'genomeBact/transcript_list.html',{'genome': genome, 'transcript': transcript})


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

def transcript_detail(request, specie, transcript):
    genome = Genome.objects.get(specie=specie)
    transcript = Transcript.objects.get(transcript=transcript)

    return render(request,'genomeBact/transcript_detail.html',{'genome':genome,'transcript': transcript})

def transcript_annot(request, transcript):
    transcript = Transcript.objects.get(transcript=transcript)

    return render(request,'genomeBact/transcript_annot.html',{'transcript': transcript})

def admin(request):

    return render(request,'genomeBact/admin.html')

def settings(request):
    
    return render(request,'genomeBact/user_settings.html')

def validator(request):
    
    return render(request,'genomeBact/validator.html')

def assign_transcript(request):
    
    return render(request,'genomeBact/assign_transcript.html')

def transcript_list_state(request):
    
    return render(request,'genomeBact/transcript_list_state.html')

def transcript_to_validate(request):
    
    return render(request,'genomeBact/transcript_to_validate.html')

def annotator(request):
    
    return render(request,'genomeBact/annotator.html')

def transcript_to_annot(request):
    
    return render(request,'genomeBact/transcript_to_annot.html')