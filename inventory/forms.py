from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Lumber, Length, Invitation

class LumberForm(forms.ModelForm):
    class Meta:
        model = Lumber
        fields = ['ref_id', 'name']

class LengthForm(forms.ModelForm):
    class Meta:
        model = Length
        fields = ['lumber', 'length', 'quantity']

class QuantityForm(forms.ModelForm):
    class Meta:
        model = Length
        fields = ['quantity']

class InvitationCodeField(forms.CharField):
    def validate(self, value):
        super().validate(value)
        try:
            invitation = Invitation.objects.get(code=value, used=False)
        except Invitation.DoesNotExist:
            raise forms.ValidationError("Invalid invitation code")

class CustomUserCreationForm(UserCreationForm):
    invitation_code = InvitationCodeField(
        help_text="Enter a valid invitation code provided by the administrator."
    )