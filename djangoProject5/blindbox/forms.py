from django import forms
from .models import BlindBox

class BlindBoxForm(forms.ModelForm):
    class Meta:
        model = BlindBox
        fields = ['title', 'description', 'category']