from django import forms


class HomeForm(forms.Form):
    text = forms.CharField()
