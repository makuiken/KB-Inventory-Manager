from django import forms
from .models import Lumber, Length

class LumberForm(forms.ModelForm):
    class Meta:
        model = Lumber
        fields = "__all__"

class LengthForm(forms.ModelForm):
    class Meta:
        model = Length
        fields = "__all__"