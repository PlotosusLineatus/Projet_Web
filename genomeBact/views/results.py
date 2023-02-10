from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from genomeBact.models import Genome,Transcript
from scripts.utils import get_max_length, get_genomes, get_genes



@login_required(login_url='login')
def results(request):

   
    '''
    # If user don't search anything from home page, return full list of genomes
    if 'user_input' in request.session:
        user_input = request.session['user_input'] 
        del request.session['user_input'] 
        # Sinon, on utilise l'input de l'user pour filtrer les génomes sur leur num d'accession
        genome = Genome.objects.filter(chromosome__contains = user_input)
        return render(request, 'genomeBact/results.html',{'genome': genome}) 
    '''

    
    # Delete session without deleting current user logs
    keys = ["accession","specie","sub_nt","sub_pep", "max","min", "query_type"]
    keys = [key for key in keys if key in request.session.keys() ]

    genomes = None
    transcripts = None

    accession = request.session["accession"]
    specie = request.session["specie"]
    sub_nt = request.session["sub_nt"]
    sub_nt = sub_nt.upper()
    sub_pep = request.session["sub_pep"]
    sub_pep = sub_pep.upper()


    # For some reason request.session doesn't store 
    # request.POST.get(name, default_integer) default_integer as integer but rather as ''

    start = request.session["start"]
    if start == '':
        start = 0
    stop = request.session["stop"]
    if stop == '':
        stop = get_max_length()

    max_ = request.session["max"]
    if max_ == '':
        max_ = get_max_length()
    min_ = request.session["min"]
    if min_ == '':
        min_ = 0

    
    ##########

    # REQUESTS

    ##########

    if request.session["query_type"] == "Genome":

        query_max = Q(length__gte = min_)
        query_min = Q(length__lte = max_)
        query_access = Q(chromosome__contains = accession)
        query_sub_nt = Q(sequence__contains = sub_nt)
        query_specie = Q(specie__contains = specie)
        query_sub_pep = Q(seq_cds__contaisn = sub_pep)

        genomes = Genome.objects.filter(query_max & query_min & query_access & query_sub_nt & query_specie)

    if request.session["query_type"] == "Transcript":
    
        query_max = Q(length_nt__gte = min_)
        query_min = Q(length_nt__lte = max_)
        query_access = Q(transcript__contains = accession)
        query_sub_nt = Q(seq_nt__contains = sub_nt)
        query_sub_pep = Q(seq_cds__contains = sub_pep)


        temp_genomes = Genome.objects.filter(specie__contains = specie)
        query_sub_species = Q(chromosome__in = temp_genomes)
        
        transcripts = Transcript.objects.filter(query_max & query_min & query_access & query_sub_nt & query_sub_pep & query_sub_species)

    # If no query by user, render all genomes 
    if genomes == transcripts:

        genomes = Genome.objects.all()
        



    ########

    # DOWNLOADS 

    ########

    if (request.method == 'POST' and genomes):

        if not genomes:

            pass

        else:
            
            # Return zip file with current genomes selected
            zip_genomes = get_genomes(genomes)
            return zip_genomes

    elif (request.method == "POST" and transcripts):

        if not transcripts:

            pass

        else:

            # Return zip file with current genes selected
            zip_genes = get_genes(transcripts)
            return zip_genes

    return render(request,'genomeBact/results.html', {'genomes': genomes, "transcripts" : transcripts}) 