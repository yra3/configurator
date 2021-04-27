from django import forms


class Configuration(forms.Form):
    name = forms.CharField()
    budget = forms.IntegerField()
