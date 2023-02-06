from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import User
'''
   _____ ______ _   _  ____  __  __ ______ 
  / ____|  ____| \ | |/ __ \|  \/  |  ____|
 | |  __| |__  |  \| | |  | | \  / | |__   
 | | |_ |  __| | . ` | |  | | |\/| |  __|  
 | |__| | |____| |\  | |__| | |  | | |____ 
  \_____|______|_| \_|\____/|_|  |_|______|
                                                                        
'''

class Genome(models.Model):

    specie = models.CharField(max_length = 50, unique = True)
    chromosome = models.CharField(max_length = 30, help_text = "Chromosome version name", primary_key=True)
    sequence = models.TextField(default = "",
                                help_text = "Copy FASTA sequence here",
                                validators=[RegexValidator(regex='^[ATCGN]+$', message = "Sequence must be ATGCN")])


    length = models.IntegerField(null = True)


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30 , unique=True)

    def __str__(self):
        return self.name

''' _____ 
           _   _  _____  _____ _____  _____ _____ _______ 
 |__   __|  __ \     /\   | \ | |/ ____|/ ____|  __ \|_   _|  __ \__   __|
    | |  | |__) |   /  \  |  \| | (___ | |    | |__) | | | | |__) | | |   
    | |  |  _  /   / /\ \ | . ` |\___ \| |    |  _  /  | | |  ___/  | |   
    | |  | | \ \  / ____ \| |\ A|____) | |____| | \ \ _| |_| |      | |   
    |_|  |_|  \_\/_/    \_\_| \_|_____/ \_____|_|  \_\_____|_|      |_|   
                                                                          
'''                                                                  
class Transcript(models.Model):
    STATUS = ( ('assigned','assigned'), ('annotated','annotated'), ('validated','validated'), ('empty','empty'))    

    # One unique ID per CDS / Protein 
    transcript = models.CharField(max_length=50, unique = True, help_text='Chromosome version name')
    chromosome = models.ForeignKey(Genome, related_name = "transcript", on_delete = models.CASCADE)
    seq_cds = models.TextField(default = "",
                                validators=[RegexValidator(regex='^[ARNDCQEGHILKMFPSTWYV]+$')])

    seq_nt = models.TextField(default = "",
                                validators=[RegexValidator(regex='^[ATCGN]+$', message = "Sequence must be ATGCN")])

    length_nt = models.IntegerField(null = True)
    length_pep = models.IntegerField(null = True)
    start = models.IntegerField(null = True)
    stop = models.IntegerField(null = True)

    ## Annotations
    gene = models.CharField(max_length= 15, default = "")
    gene_biotype =  models.CharField(max_length=10, default = "")
    transcript_biotype = models.CharField(max_length= 15, default = "")
    gene_symbol = models.CharField(max_length=10, default = "")
    description = models.CharField(max_length=100, default = "")    

    status = models.CharField(max_length=200, choices=STATUS, default='empty')
    status_date = models.DateTimeField(null = True)
    annotator = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name="to_annotate")
    validator = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    FilterFields = ["length"]




