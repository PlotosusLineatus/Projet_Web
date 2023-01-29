from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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

class UploadFileForm(forms.Form):

    file = forms.FileField()

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']