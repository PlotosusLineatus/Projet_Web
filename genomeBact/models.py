from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True
User._meta.get_field('email')._required = True


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
    name = models.CharField(max_length=30 , unique=True) ## A SUPP


    STATUS = ( ('Admin','Admin'), ('Annotateur','Annotateur'), ('Validateur','Validateur'), ('Lecteur','Lecteur'))
    group = models.CharField(max_length=40, choices=STATUS, default='Lecteur')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) 
    last_connexion = models.DateTimeField()

    def __str__(self):
        return self.name

class Connexion(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField()

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
    chromosome = models.ForeignKey(Genome, related_name = "transcript", on_delete = models.CASCADE)
    
    # One unique ID per CDS / Protein 
    transcript = models.CharField(max_length=50, unique = True, help_text='Chromosome version name')
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
    validator = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name ="to_validate")
    message = models.CharField(max_length=100, default = "")    
    
    FilterFields = ["length"]

    @property
    def length(self):
        return (self.stop - self.start)+1




