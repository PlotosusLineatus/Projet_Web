import os
from genomeBact.models import Genome
import io
import zipfile
from django.http import HttpResponse, FileResponse

def handle_uploaded_file(f):

    '''
    Deprecated function, no time for upload file function
    '''
    with open((os.getcwd() + "/temp_dir"), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def to_fasta_format(sequence, line_width=60):

    '''
    Input any string and return to FASTA format with line width specified
    '''
    fasta_format = ""
    for i in range(0, len(sequence), line_width):
        fasta_format += sequence[i:i+line_width] + "\n"
    return fasta_format


def get_genomes(genomes):

    '''
    Return FileResponse containing zip file containing each genome as solo FASTA file
    '''

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode='w') as zip_file:

        for genome in genomes:

            fasta_file = io.StringIO()
            header = generate_header(genome)
            fasta_file.write(f">{header}\n")
    
            formated_seq = to_fasta_format(genome.sequence)
            fasta_file.write(formated_seq)

            zip_file.writestr(f"{genome.specie}.fasta", fasta_file.getvalue())

    buffer.seek(0)
    response = FileResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="genomes.zip"'
    return(response)

def get_genes(genes):

    '''
    Return FileResponse containing zip file of all transcripts downloaded.
    Two files : one for peptidic sequence and one for nucleotidic one.

    '''

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode='w') as zip_file:
        pep_file = io.StringIO()
        cds_file = io.StringIO()
        for gene in genes:

            header = generate_header(gene, "pep")
            pep_file.write(f">{header}\n")
            formated_seq = to_fasta_format(gene.seq_cds)
            pep_file.write(formated_seq)

            header = generate_header(gene, "cds")
            cds_file.write(f">{header}\n")
            formated_seq = to_fasta_format(gene.seq_nt)
            cds_file.write(formated_seq)

        zip_file.writestr(f"genes_coding_sequences.fasta", cds_file.getvalue())
        zip_file.writestr(f"genes_peptide_sequences.fasta", pep_file.getvalue())

    buffer.seek(0)
    response = FileResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="genes.zip"'
    return(response)

def generate_header(instance, type_ = ""):

    '''
    Generate FASTA header respecting the regex of the database. 
    Different header if genome or genes.
    '''
    if ( type_ == "pep" or type_ == "cds"):

        # >AAN78501 cds chromosome:ASM744v1:Chromosome:190:255:1 
        header = []
        header.append(instance.transcript + " " + type_ + " " + "chromosome:" + instance.chromosome.chromosome + ":" + str(instance.start) + ":" + str(instance.stop) + ":1")
        annotations = ["gene","gene_biotype_","transcript_biotype","gene_symbol","description"]

        # gene:c5491 gene_biotype:protein_coding transcript_biotype:protein_coding gene_symbol:thrL description:Thr operon leader peptide
        for field_name in instance.__dict__:

            if ( not field_name.startswith('_') and field_name in annotations and instance.__dict__[field_name] != ""):

                header.append(field_name + ":" + instance.__dict__[field_name]) 


        header = " ".join(header)

    else:

        # >Chromosome dna:chromosome chromosome:ASM744v1:Chromosome:1:5231428:1 REF
        header = ("Chromosome dna:chromosome chromosome:" + instance.chromosome + ":Chromosome:1:" + str(instance.length) + ":1 REF")
    return header

def get_annotation(description):

    '''
    Get annotations availables in a given header respecting the format of the database.
    '''

    import re

    annot = {}
    annot["gene"] = re.search(r"gene:(\w+)", description).group(1) if re.search(r"gene:(\w+)", description) else ""
    annot["gene_biotype"] = re.search(r"gene_biotype:(\w+)", description).group(1) if re.search(r"gene_biotype:(\w+)", description) else ""
    annot["transcript_biotype"] = re.search(r"transcript_biotype:(\w+)", description).group(1) if re.search(r"transcript_biotype:(\w+)", description) else ""
    annot["gene_symbol"] = re.search(r"gene_symbol:(\w+)", description).group(1) if re.search(r"gene_symbol:(\w+)", description) else ""
    annot["description"] = re.search(r"description:([\w*\s]*)", description).group(1) if re.search(r"description:([\w*\s]*)", description) else ""

    return annot

def get_start_stop(description):
    

    '''
    Get start and stop position of gene on its chromosome
    '''
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

    '''
    Get accession number of chromosome
    '''

    import re

    match = re.search(r"chromosome:(\w+)", description)
    temp = match.group(1)

    try: 
        len(temp) == 1
        return temp

    except AssertionError:
        
        print("Mauvais parsing du header du génome de  : %s" % description)
        return None



def get_data(absolute_path = "./data"):
#def get_data(absolute_path = "/home/noemie/Documents/data"):
#def get_data(absolute_path = "/home/sherman/Documents/M2/WEB/data"):

    '''
    Use all previous functions to store sequences in the absolute path in dict
    '''

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
            annot = get_annotation(seq.description)

            
            seq_dict[seq.name]["start"] = terms[0]
            seq_dict[seq.name]["stop"] = terms[1]
            seq_dict[seq.name]["NT"] = str(seq.seq)
            seq_dict[seq.name]["specie"] = strain
            seq_dict[seq.name]["gene"] = annot["gene"]
            seq_dict[seq.name]["gene_biotype"] = annot["gene_biotype"]
            seq_dict[seq.name]["transcript_biotype"] = annot["transcript_biotype"]
            seq_dict[seq.name]["gene_symbol"] = annot["gene_symbol"]
            seq_dict[seq.name]["description"] = annot["description"]
            
            
            
    
    for file in pep_files :
        
        strain = file.replace("_pep.fa", "" )
        
        
        sequences = SeqIO.parse(file, "fasta")
        for seq in sequences:
            
            if seq.name not in seq_dict:
                
                raise Exception("Peptide without CDS : %s of %s" % (seq.description, strain))

            else :
                
                
                if seq_dict[seq.name]["specie"] == strain : 
                                
                    seq_dict[seq.name]["AA"] = str(seq.seq)
                    
                else : 
                    
                    raise Exception("Same transcr_ID for different strains")

    
    full_dict = {}
    full_dict["genomes"] = genome_dict
    full_dict["transcripts"] = seq_dict

    return full_dict

def get_max_length() -> int:

    '''
    Compute max length of all available genomes in database for default query values.
    '''

    _list = []
    g = Genome.objects.all()

    for item in g:
        _list.append(item.length)

    return max(_list)