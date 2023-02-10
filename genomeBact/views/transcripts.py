from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Now
from django.http import HttpResponse, HttpResponseRedirect

from Bio import SeqIO
from io import StringIO
from genomeBact.models import Genome,Transcript
from genomeBact.forms import GenomeForm, TranscriptForm, UploadFileForm, AnnotForm
from genomeBact.decorators import admin_only

from scripts.utils import  get_genes


@login_required(login_url='login')
@admin_only
def genome_create(request):

    if request.method == 'POST':
        form = GenomeForm(request.POST)  
        if form.is_valid():
            genome = form.save()
            #return redirect('transcript-list', genome.specie)
            return redirect('genome-detail', genome.specie)
    else:
        form = GenomeForm()

    return render(request,'genomeBact/genome_create.html',{'form': form}) 

@login_required(login_url='login')
def genome_detail(request, specie):
    try:
        genome = Genome.objects.get(specie=specie)
    except Genome.DoesNotExist:
        return redirect('home')
    try:
        transcripts = Transcript.objects.filter(chromosome = genome.chromosome)
    except Transcript.DoesNotExist:
        return redirect('home')

    if request.method == 'POST' and 'Delete' in request.POST:
        genome.delete()
        messages.success(request, "The genome "+ genome.specie + " was deleted.")
        return redirect('results')

     # Download transcripts of genome 
    if request.method == "POST" and "Download" in request.POST:

        if not transcripts:

            pass

        else:

            # Return zip file with current genes selected
            zip_genes = get_genes(transcripts)
            return zip_genes
    
    return render(request,'genomeBact/genome_detail.html',{'genome': genome, 'transcripts' : transcripts})
    
@login_required(login_url='login')
@admin_only
def transcript_create(request):
    genomes = Genome.objects.all

    if request.method == 'POST':
        form = TranscriptForm(request.POST)  
        if form.is_valid():
            specie = request.POST.get("genome")
            try : 
                genome = Genome.objects.get(specie=specie)
                form.instance.chromosome = genome
                transcript = form.save()

                messages.success(request, "The transcript "+ transcript.transcript + " wad added to "+specie)
                return redirect('admin')
            except Genome.DoesNotExist:
                messages.info(request, "Select the genome." )
    else:
        form = TranscriptForm()

    context = {'form': form, "genomes" : genomes}
    return render(request,'genomeBact/transcript_create.html', context) 

@login_required(login_url='login')
def transcript_detail(request, specie, transcript):

    try:
        genome = Genome.objects.get(specie=specie)
    except Genome.DoesNotExist:
        return redirect('home')
    try:
        cds = Transcript.objects.get(transcript=transcript)
    except Transcript.DoesNotExist:
        return redirect('home')

    list = []
    list.append(cds)
    if request.method == 'POST':
        form = AnnotForm(request.POST)

        if "Download" in request.POST:
            if not list:
                pass
            else:
                # Return zip file with current genes selected
                zip_genes = get_genes(list)
                return zip_genes
                
        elif 'Validate' in request.POST:
            Transcript.objects.filter(transcript=transcript).update(status = 'validated', status_date = Now(), annotator=None)
            messages.success(request, 'Annotations were validated.')
            return HttpResponseRedirect(request.path_info)
        elif 'to_validate' in request.POST:
            Transcript.objects.filter(transcript=transcript).update(status = 'annotated', status_date = Now())
            messages.success(request, 'Annotations were send for validation.')
            return HttpResponseRedirect(request.path_info)
        elif 'reject_validation' in request.POST:
            message = request.POST.get("message")
            Transcript.objects.filter(transcript=transcript).update(status = 'assigned', status_date = Now(), message = message)
            messages.success(request, 'Annotations were send back to '+ cds.annotator.name )
            return HttpResponseRedirect(request.path_info)
        elif 'Delete' in request.POST:
            cds.delete()
            messages.success(request, "The transcript "+ cds.transcript + " from "+ specie +" was deleted.")
            return redirect('results')
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