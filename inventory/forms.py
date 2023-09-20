from django import forms
from .models import Lumber, Length

class LumberForm(forms.ModelForm):
    class Meta:
        model = Lumber
        fields = ['ref_id', 'name']

class LengthForm(forms.ModelForm):
    class Meta:
        model = Length
        fields = ['ref_id', 'length', 'quantity']