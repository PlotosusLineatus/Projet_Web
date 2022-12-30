from django.shortcuts import redirect, render
from django.http import HttpResponse
from genomeBact.models import Genome
from genomeBact.forms import GenomeForm

def genome_list(request):
    genomes = Genome.objects.all()
    return render(request, 'genomeBact/genome_list.html',{'genomes': genomes})

def genome_create(request):
    if request.method == 'POST':
        print('HELLOOO')
        form = GenomeForm(request.POST)  
        if form.is_valid():
            new_genome = form.save()
            return redirect('genome-list')
            #return redirect('genome-details', new_genome.id)
    else:
        print("ellllllse")
        form = GenomeForm()

    return render(request,'genomeBact/genome_create.html',{'form': form}) 