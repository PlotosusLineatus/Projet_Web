from django.shortcuts import redirect, render
from django.http import HttpResponse
from genomeBact.models import Genome
from genomeBact.forms import GenomeForm

def genome_list(request):
    genomes = Genome.objects.all()
    return render(request, 'genomeBact/genome_list.html',{'genomes': genomes})

def genome_detail(request, specie):
    genome = Genome.objects.get(specie=specie)

    return render(request,'genomeBact/genome_detail.html',{'genome': genome})

def genome_create(request):
    if request.method == 'POST':
        form = GenomeForm(request.POST)  
        if form.is_valid():
            new_genome = form.save()
            return redirect('genome-list')
            #return redirect('genome-details', new_genome.id)
    else:
        form = GenomeForm()

    return render(request,'genomeBact/genome_create.html',{'form': form}) 

def genome_delete(request, specie):
    genome = Genome.objects.get(specie=specie)
    
    if request.method == 'POST':
        genome.delete()
        return redirect('genome-list')

    return render(request,'genomeBact/genome_delete.html',{'genome': genome})
