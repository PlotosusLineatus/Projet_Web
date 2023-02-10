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
    transcript = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter chromosome name'}))
    seq_cds = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter protein sequence'}),
                                validators=[RegexValidator(regex='^[ARNDCQEGHILKMFPSTWYV]+$', message = "Sequence must be ARNDCQEGHILKMFPSTWYV")])

    seq_nt = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter NT sequence'}),
                                validators=[RegexValidator(regex='^[ATCGN]+$', message = "Sequence must be ATGCN")])
    class Meta:
        model = Transcript
        fields = ['transcript', 'seq_cds', 'seq_nt', 'length_nt', 'length_pep', 'start', 'stop']

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
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter same password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CreateProfileForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter first name'}), max_length=30)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter last name'}), max_length=150)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'}), validators=[phone_regex], max_length=17) 
    group = forms.ChoiceField(widget = forms.Select(), 
                 choices = ([('Lecteur','Lecteur'), ('Annotateur','Annotateur'), ('Validateur','Validateur'), ]), initial='Lecteur')
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number', 'group']

class ModifyUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter email'}), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter same password'}), required=False)

    class Meta:
        model = User
        fields = ['email', 'password1', "password2"]

class ProfileForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter first name'}), max_length=30, required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter last name'}), max_length=150, required=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'}), validators=[phone_regex], max_length=17, required=False) 
    group = forms.ChoiceField(widget = forms.Select(), 
                 choices = ([('Lecteur','Lecteur'), ('Annotateur','Annotateur'), ('Validateur','Validateur'), ]), initial='Lecteur')
    
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number','group']
