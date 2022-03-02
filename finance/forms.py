from django import forms
from django.forms import ModelForm
from .models import Operation


class OperationCreateForm(ModelForm):
    class Meta:
        model = Operation
        fields = ['sum', 'wallet', 'wallet_recipient', 'type', 'category', 'date', 'description']
