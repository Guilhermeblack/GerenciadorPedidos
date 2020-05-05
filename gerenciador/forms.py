from django import forms
from . import models
from django.contrib.auth.hashers import make_password, check_password

class autForm(forms.ModelForm):
    class Meta:
        model = models.logform
        fields = ('nome', 'senha')

    # nome = forms.CharField(max_length=50, null=False, blank=False,)
    senha = forms.CharField(widget=forms.PasswordInput)