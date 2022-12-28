from django.contrib import admin

from genomeBact.models import Genome

class GenomeAdmin(admin.ModelAdmin):
    list_display = ('specie', 'chromosome', 'size') 

admin.site.register(Genome)