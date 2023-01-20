from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

class Genome(models.Model):


    strain = models.CharField(max_length = 50, unique = True)
    chromosome = models.CharField(max_length = 30, help_text = "Chromosome version name", default = "")
    sequence = models.TextField(default = "",
                                help_text = "Copy FASTA sequence here",
                                validators=[RegexValidator(regex='^[ATCGN]+$', message = "Sequence must be ATGCN")])

#    def get_absolute_url(self):
#        return reverse('model-detail-view', args=[str(self.chromosome)])

class Transcript(models.Model):
    
    ## Physical informations 

    # One unique ID per CDS / Protein 
    name = models.CharField(max_length=50, unique = True)
    genome = models.ForeignKey(Genome, related_name = "transcript", on_delete = models.CASCADE)
    seq_cds = models.TextField(default = "",
                                validators=[RegexValidator(regex='^[ARNDCQEGHILKMFPSTWYV]+$')])

    seq_nt = models.TextField(default = "",
                                validators=[RegexValidator(regex='^[ATCGN]+$', message = "Sequence must be ATGCN")])
    start = models.IntegerField(null = True)
    stop = models.IntegerField(null = True)
