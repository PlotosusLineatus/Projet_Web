from django.shortcuts import render
from django.http import HttpResponse
from genomeBact.models import Genome
from genomeBact.forms import GenomeForm

def genome_list(request):
    genomes = Genome.objects.all()
    return render(request, 'genomeBact/genome_list.html',{'genomes': genomes})

def genome_create(request):
    form = GenomeForm()  
    return render(request,'genomeBact/genome_create.html',{'form': form}) 