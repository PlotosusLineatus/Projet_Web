from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from genomeBact.models import Genome, Transcript , Profile
from django.core.validators import RegexValidator

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

class ModifyUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter email'}), required=False)
    password1 = forms.CharField(required = False)
    password2 = forms.CharField(required = False)
    class Meta:
        model = User
        fields = ['email']

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=17, required=False) 
    group = forms.CharField(required=False)
    
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number']
