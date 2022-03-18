from email.policy import default
from tabnanny import verbose
from django import forms
from django.forms import ModelForm
from .models import Operation
from datetime import datetime


class OperationCreateForm(ModelForm):
    date = forms.DateTimeField(label='Дата', input_formats=['%d.%m.%Y %H:%M'], initial=datetime.now)
    class Meta:
        model = Operation
        fields = ['sum', 'wallet', 'wallet_recipient', 'type', 'category', 'date', 'description']

class OperationUpdateForm(ModelForm):
    date = forms.DateTimeField(label='Дата', input_formats=['%d.%m.%Y %H:%M'], initial=datetime.now)
    class Meta:
        model = Operation
        fields = ['sum', 'wallet', 'wallet_recipient', 'type', 'category', 'date', 'description']
        
