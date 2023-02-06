from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from genomeBact.models import Genome, Transcript , Profile

class GenomeForm(forms.ModelForm):
    class Meta:
        model = Genome
        fields = '__all__'

class TranscriptForm(forms.ModelForm):
    class Meta:
        model = Transcript
        #fields = '__all__'
        exclude = ('chromosome',)

class AnnotForm(forms.ModelForm):

    gene = forms.CharField(required=False)
    gene_biotype =  forms.CharField(required=False)
    transcript_biotype = forms.CharField(required=False)
    gene_symbol = forms.CharField(required=False)
    description = forms.CharField(required=False)
    
    class Meta:
        model = Transcript
        fields = ['gene', 'gene_biotype', 'transcript_biotype', 'gene_symbol', 'description']

class UploadFileForm(forms.Form):

    file = forms.FileField()

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.Form):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number']
