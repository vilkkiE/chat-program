from django import forms
from django.forms import ModelForm
from .models import Channel


class ChannelForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)