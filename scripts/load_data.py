from genomeBact.models import Genome, Transcript, Annotation 
import os, glob
from Bio import SeqIO

         
# Mandatory run() procedure name, runscript doest not recognize if not
def run(): 

	os.chdir("/home/sherman/Documents/M2/WEB/data")
	
	cds = glob.glob("*cds*")
	protein = glob.glob("*pep*")
	full = glob.glob("*")

	# Get only genome files names
	gen = [item for item in full if item not in protein]
	gen = [item for item in gen if item not in cds]
	
	for file in gen:
	
		for genome in SeqIO.parse(file, "fasta"):
		
			print(genome.description)
		
