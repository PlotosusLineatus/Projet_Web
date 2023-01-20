from django import forms
from genomeBact.models import Genome, Transcript 

class GenomeForm(forms.ModelForm):
    class Meta:
        model = Genome
        fields = "__all__"


class TranscriptSequenceField(forms.CharField):

    def __init__(self, *args, **kwargs):
        self.genome = kwargs.pop("genome", None)
        super().__init__(*args, **kwargs)

    def clean(self, value):
        cleaned_data = super().clean(value)
        
        if self.genome:
            if len(cleaned_data) > len(self.genome.sequence):
                raise forms.ValidationError("Transcript sequence must be shorter than the genome it comes from.")
        return cleaned_data


class TranscriptForm(forms.ModelForm):
    sequence = TranscriptSequenceField()

    class Meta:
        model = Transcript
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sequence'].genome = self.instance.genome