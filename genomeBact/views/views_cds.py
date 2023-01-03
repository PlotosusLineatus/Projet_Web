from django.shortcuts import redirect, render
from genomeBact.models import Genome,Transcript
from genomeBact.forms import GenomeForm, TranscriptForm

def cds_list(request, specie):
    genome = Genome.objects.get(specie=specie)
    cds = Transcript.objects.filter(chromosome = genome.chromosome)

    return render(request, 'genomeBact/cds_list.html',{'transcript': cds, 'genome' : genome})

def cds_create(request, specie):
    genome = Genome.objects.get(specie=specie)

    if request.method == 'POST':
        form = TranscriptForm(request.POST)  
        if form.is_valid():
            form.instance.chromosome = genome
            new_cds = form.save()
            return redirect('cds-list', genome.specie)
    else:
        form = TranscriptForm()

    return render(request,'genomeBact/cds_create.html',{'form': form, 'genome' : genome}) 
