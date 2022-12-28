from django import forms
from genomeBact.models import Genome

class GenomeForm(forms.ModelForm):
    class Meta:
        model = Genome
        fields = '__all__'