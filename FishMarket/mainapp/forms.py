from django import forms
from django.forms import Form

class SearchForm(Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пошук товару'}))