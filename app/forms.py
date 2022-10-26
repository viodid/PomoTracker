# forms.py
from django import forms


class ProfileForm(forms.Form):
    image = forms.ImageField(required=True, label='Upload profile picture')
