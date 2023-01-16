from genomeBact.models import Transcript
from django.db import transaction

# Penser à regarder la disposition management/commands comme alternative à runscript

def get_term(description):
    
    
    import re
    
    # Est attendu un pattern comme *Chromosome:1:5528445:1* dans tous les headers des FASTAs
    match = re.search(r':(\d+:\d+)', description)
    _ =  match.group(1).split(":")
    _ = list(map(int, _))

    try: 
        len(_) == 2
        return _

    except AssertionError:
        
        print("Oopsie : %s" % description)
        return None


def get_set(absolute_path = "/home/sherman/Documents/M2/WEB/data"):


    import os
    from Bio import SeqIO

    os.chdir(absolute_path)
        
    file_list = os.listdir()

    cds_files = [file for file in file_list if "_cds" in file]
    pep_files = [file for file in file_list if "_pep" in file]
    other_files = [file for file in file_list if "_cds" not in file and "_pep" not in file]


    seq_dict = {}

    for file in cds_files :
        
        specie = file.replace("_cds.fa", "" )
        sequences = SeqIO.parse(file, "fasta")
        
        for seq in sequences:
                
            seq_dict[seq.name] = {}
        
            terms = get_term(seq.description)
            
            seq_dict[seq.name]["start"] = terms[0]
            seq_dict[seq.name]["stop"] = terms[1]
            seq_dict[seq.name]["NT"] = str(seq.seq)
            seq_dict[seq.name]["specie"] = specie
            
            
    
    for file in pep_files :
        
        specie = file.replace("_pep.fa", "" )
        
        
        sequences = SeqIO.parse(file, "fasta")
        for seq in sequences:
            
            if seq.name not in seq_dict:
                
                raise Exception("Peptide without CDS")

            else :
                
                
                if seq_dict[seq.name]["specie"] == specie : 
                                
                    seq_dict[seq.name]["AA"] = str(seq.seq)
                    
                else : 
                    
                    raise Exception("Same transcr_ID for different strains")

    return seq_dict


def run():

    try:

        a = get_set()

    except AssertionError:

        print("Erreur du chargement des CDS et des peptides depuis le multiFASTA")


    data = []
    
    for seq_id in a.keys():

        data.append(Transcript(sequence = a[seq_id]["NT"],
                                specie = a[seq_id]["specie"],
                                name = seq_id,
                                start = a[seq_id]["start"],
                                stop = a[seq_id]["stop"]))

    with transaction.atomic():

        Transcript.objects.bulk_create(data)