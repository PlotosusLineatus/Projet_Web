from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
import Bio




class testClass(models.Model):

    field1 = models.CharField(default= "", max_length=50)

    def show(self):

        return ("Field : %s" % self.field1)


class Genome(models.Model):


    strain = models.CharField(max_length = 50, default = "")  # Not unique because of several strains, experimental conditions etc : bact. adaptation very quick
    chromosome = models.CharField(max_length = 30, primary_key= True, help_text = "Chromosome version name")
    sequence = models.TextField(default = "", help_text = "Copy FASTA sequence here")

    def show(self):
        print(self.chromosome)
        print(self.strain)

    @property
    def length(self): 
        return len(self.sequence)
        
#    def get_absolute_url(self):
#        return reverse('model-detail-view', args=[str(self.chromosome)])

class Transcript(models.Model):
    
    ## Physical informations 

    # One unique ID per CDS / Protein 
    ID = models.CharField(max_length=50, primary_key= True)
    seq_cds = models.TextField(default = "")
    seq_nt = models.TextField(default = "")

    chromosome = models.ForeignKey(Genome, null= False, on_delete=models.CASCADE)    

    start = models.IntegerField(null = True)
    stop = models.IntegerField(null = True)

    ## Annotation 
    gene = models.CharField(max_length = 10, null = True)
    gene_biotype = models.CharField(max_length = 100, default = "protein coding")
    description = models.CharField(max_length = 100, default = "")

    # Not functionnal : can validate 
    gene_symbol = models.CharField(max_length = 20, null = True, validators=[RegexValidator("^[A-Za-z0-9]+$", message= "OLAAAAAAAA OH")])


    # Calculate length and store it as field as Transcript.length return actual length
    @property
    def length(self):
        return self.stop - self.start

    def show(self):
            print(self.ID)
            print(self.gene)
            print(self.gene_symbol)
            print(self.length)
    

class Annotation(models.Model):
    transcript = models.ForeignKey(Transcript, null=False, on_delete=models.CASCADE)
    gene = models.CharField(max_length= 15, primary_key=True)
    gene_biotype =  models.CharField(max_length=10)
    transcript_biotype = models.CharField(max_length= 15)
    gene_symbol = models.CharField(max_length=10)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.gene

