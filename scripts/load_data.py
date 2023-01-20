from django.core import management
from genomeBact.models import Transcript, Genome
from django.db import transaction


# Penser à regarder la disposition management/commands comme alternative à runscript

def get_start_stop(description):
    
    import re
    
    # Est attendu un pattern comme *Chromosome:1:5528445:1* dans tous les headers des FASTAs
    match = re.search(r':(\d+:\d+)', description)
    temp =  match.group(1).split(":")
    temp = list(map(int, temp))

    try: 
        len(temp) == 2
        return temp

    except AssertionError:
        
        print("Oopsie : %s" % description)
        return None

def get_chromosome(description):

    import re

    match = re.search(r"chromosome:(\w+)", description)
    temp = match.group(1)

    try: 
        len(temp) == 1
        return temp

    except AssertionError:
        
        print("Mauvais parsing du header du génome de  : %s" % description)
        return None

def get_data(absolute_path = "/home/sherman/Documents/M2/WEB/data"):


    import os
    from Bio import SeqIO

    os.chdir(absolute_path)
        
    file_list = os.listdir()

    cds_files = [file for file in file_list if "_cds" in file]
    pep_files = [file for file in file_list if "_pep" in file]
    other_files = [file for file in file_list if "_cds" not in file and "_pep" not in file]



    genome_dict = {}

    for file in other_files: 

        strain = file.replace(".fa","")
        sequence = SeqIO.parse(file,"fasta")

        for seq in sequence:

            
            genome_dict[strain] = {}
            genome_dict[strain]["chromosome"] = get_chromosome(seq.description)
            genome_dict[strain]["sequence"] = str(seq.seq)
            



    seq_dict = {}

    for file in cds_files :
        
        strain = file.replace("_cds.fa", "" )
        sequences = SeqIO.parse(file, "fasta")
        
        for seq in sequences:
                
            seq_dict[seq.name] = {}
        
            terms = get_start_stop(seq.description)
            
            seq_dict[seq.name]["start"] = terms[0]
            seq_dict[seq.name]["stop"] = terms[1]
            seq_dict[seq.name]["NT"] = str(seq.seq)
            seq_dict[seq.name]["strain"] = strain
            
            
    
    for file in pep_files :
        
        strain = file.replace("_pep.fa", "" )
        
        
        sequences = SeqIO.parse(file, "fasta")
        for seq in sequences:
            
            if seq.name not in seq_dict:
                
                raise Exception("Peptide without CDS : %s of %s" % (seq.description, strain))

            else :
                
                
                if seq_dict[seq.name]["strain"] == strain : 
                                
                    seq_dict[seq.name]["AA"] = str(seq.seq)
                    
                else : 
                    
                    raise Exception("Same transcr_ID for different strains")

    
    full_dict = {}
    full_dict["genomes"] = genome_dict
    full_dict["transcripts"] = seq_dict

    return full_dict

	


def run():

    try:

        full_dict = get_data()

    except AssertionError:

        print("Erreur du chargement des CDS et des peptides depuis le multiFASTA")


    if (Transcript.objects.all().exists() | Genome.objects.all().exists()):

        print("La base de données n'est pas vide, le chargement des données initiales requiert vider cette dernière")

        management.call_command("flush")

    genomes_data = []
    genome_dict = full_dict["genomes"]

    for strain in genome_dict.keys():

        genomes_data.append(Genome(sequence = genome_dict[strain]["sequence"],
                                chromosome = genome_dict[strain]["chromosome"],
                                strain = strain))

    with transaction.atomic():
        Genome.objects.bulk_create(genomes_data)



    transcripts_dict = full_dict["transcripts"]

    for temp_strain in genome_dict.keys():

        current_genome = Genome.objects.get(strain = temp_strain)

        transcripts_of_current_genome = []

        for tsc_name in transcripts_dict.keys():

            if ( transcripts_dict[tsc_name]["strain"] == temp_strain ):

                transcripts_of_current_genome.append(Transcript(name = tsc_name, 
                                                                genome = current_genome,
                                                                seq_cds = transcripts_dict[tsc_name]["AA"],
                                                                seq_nt = transcripts_dict[tsc_name]["NT"],
                                                                start = transcripts_dict[tsc_name]["start"],
                                                                stop = transcripts_dict[tsc_name]["stop"]))

        Transcript.objects.bulk_create(transcripts_of_current_genome)

