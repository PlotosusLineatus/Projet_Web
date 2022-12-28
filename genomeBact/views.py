from django.shortcuts import render
from django.http import HttpResponse
from genomeBact.models import Genome

def genome_list(request):
    genomes = Genome.objects.all()
    return render(request, 'genomeBact/genome_list.html',
														{'genomes': genomes})