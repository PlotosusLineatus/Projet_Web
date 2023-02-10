from django.core import management
from genomeBact.models import Transcript, Genome
from django.db import transaction
from scripts.utils import *


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
                                length = len(genome_dict[strain]["sequence"]),
                                specie = strain))

    Genome.objects.bulk_create(genomes_data)



    transcripts_dict = full_dict["transcripts"]

    for temp_strain in genome_dict.keys():

        current_chromosome = Genome.objects.get(specie = temp_strain)

        transcripts_of_current_genome = []

        for tsc_name in transcripts_dict.keys():

            if ( transcripts_dict[tsc_name]["specie"] == temp_strain ):

                transcripts_of_current_genome.append(Transcript(transcript = tsc_name, 
                                                                chromosome = current_chromosome,
                                                                seq_cds = transcripts_dict[tsc_name]["AA"],
                                                                seq_nt = transcripts_dict[tsc_name]["NT"],
                                                                start = transcripts_dict[tsc_name]["start"],
                                                                stop = transcripts_dict[tsc_name]["stop"],
                                                                length_nt = int(len(transcripts_dict[tsc_name]["NT"])),
                                                                length_pep = int(len(transcripts_dict[tsc_name]["AA"])),
                                                                gene = transcripts_dict[tsc_name]["gene"],
                                                                gene_biotype = transcripts_dict[tsc_name]["gene_biotype"],
                                                                transcript_biotype = transcripts_dict[tsc_name]["transcript_biotype"],
                                                                gene_symbol = transcripts_dict[tsc_name]["gene_symbol"],
                                                                description = transcripts_dict[tsc_name]["description"]))
                                     

        Transcript.objects.bulk_create(transcripts_of_current_genome)