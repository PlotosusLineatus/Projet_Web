from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

class Genome(models.Model):
    specie = models.CharField(max_length=50, unique= True)    ## prokaryote only so 'unique = True'
    chromosome = models.CharField(max_length= 30, primary_key= True, help_text = "Chromosome name")
    size =  models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100000000)], help_text = "Size of chromosome")
    start = models.IntegerField( default= 1, validators= [MinValueValidator(1),MaxValueValidator(100000000)])
    # direction ? 

    def __str__(self):
        return self.chromosome
        
#    def get_absolute_url(self):
#        return reverse('model-detail-view', args=[str(self.chromosome)])

class Transcript(models.Model):
    transcript = models.CharField(max_length=50, primary_key= True)
    chromosome = models.ForeignKey(Genome, null= False, on_delete=models.CASCADE)
    start =  models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100000000)])
    stop =  models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100000000)])
    gene = models.CharField(max_length= 15, unique=True)
    gene_biotype =  models.CharField(max_length=10)
    transcript_biotype = models.CharField(max_length= 15)
    gene_symbol = models.CharField(max_length=10)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.transcript

