from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

class Genome(models.Model):
    specie = models.CharField(max_length=50, unique= True, help_text='*')    ## prokaryote only so 'unique = True'
    chromosome = models.CharField(max_length= 30, primary_key= True, help_text='*')
    size =  models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100000000)], help_text='*')
    # direction ? 

    def __str__(self):
        return self.chromosome
        
#    def get_absolute_url(self):
#        return reverse('model-detail-view', args=[str(self.chromosome)])

class Transcript(models.Model):
    transcript = models.CharField(max_length=50, primary_key= True, help_text='*')
    chromosome = models.ForeignKey(Genome, null= False, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.transcript
"""
    start =  models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100000000)], help_text='*')
    stop =  models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100000000)], help_text='*')
    gene = models.CharField(max_length= 15, unique=True, help_text='*')
    gene_biotype =  models.CharField(max_length=10, default="")
    transcript_biotype = models.CharField(max_length= 15, default="")
    gene_symbol = models.CharField(max_length=10, default="")
    description = models.CharField(max_length=100, default="")
"""

