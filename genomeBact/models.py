from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

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
    chromosome = models.CharField(max_length = 30, help_text = "Chromosome version name", default = "", primary_key=True)
    sequence = models.TextField(default = "",
                                help_text = "Copy FASTA sequence here",
                                validators=[RegexValidator(regex='^[ATCGN]+$', message = "Sequence must be ATGCN")])


    @property
    def length(self):
        return len(self.sequence)




''' _____ 
           _   _  _____  _____ _____  _____ _____ _______ 
 |__   __|  __ \     /\   | \ | |/ ____|/ ____|  __ \|_   _|  __ \__   __|
    | |  | |__) |   /  \  |  \| | (___ | |    | |__) | | | | |__) | | |   
    | |  |  _  /   / /\ \ | . ` |\___ \| |    |  _  /  | | |  ___/  | |   
    | |  | | \ \  / ____ \| |\ A|____) | |____| | \ \ _| |_| |      | |   
    |_|  |_|  \_\/_/    \_\_| \_|_____/ \_____|_|  \_\_____|_|      |_|   
                                                                          
'''                                                                  
class Transcript(models.Model):
    

    # One unique ID per CDS / Protein 
    transcript = models.CharField(max_length=50, unique = True, help_text='Chromosome version name')
    chromosome = models.ForeignKey(Genome, related_name = "transcript", on_delete = models.CASCADE)
    seq_cds = models.TextField(default = "",
                                validators=[RegexValidator(regex='^[ARNDCQEGHILKMFPSTWYV]+$')])

    seq_nt = models.TextField(default = "",
                                validators=[RegexValidator(regex='^[ATCGN]+$', message = "Sequence must be ATGCN")])
    start = models.IntegerField(null = True)
    stop = models.IntegerField(null = True)

    @property
    def nt_length(self):
        return len(self.seq_nt)

    @property
    def pep_length(self):
        return len(self.seq_cds)


