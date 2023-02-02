import os
from Bio import SeqIO
from Bio.Blast import NCBIWWW, NCBIXML



NCBIWWW.email = "herman.simon.lm@gmail.com"

os.chdir("/home/sherman")


seq = SeqIO.read("test.txt","fasta")


result_handle = NCBIWWW.qblast("blastn", "nt", seq.seq)

blast_record = NCBIXML.parse(result_handle)
for alignment in blast_record.alignments:
    for hsp in alignment.hsps:
        print(hsp.strand)