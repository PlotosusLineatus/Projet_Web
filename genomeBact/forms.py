from django import forms
from genomeBact.models import Genome, Transcript 

class GenomeForm(forms.ModelForm):
    class Meta:
        model = Genome
        fields = '__all__'

class TranscriptForm(forms.ModelForm):
    class Meta:
        model = Transcript
        #fields = '__all__'
        exclude = ('chromosome',)