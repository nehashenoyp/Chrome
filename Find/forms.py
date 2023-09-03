# myapp/forms.py
from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='', max_length=100)

class PathForm(forms.Form):
    path = forms.CharField(label='',max_length=100)
    
