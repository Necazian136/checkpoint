from django import forms


class PlateForm(forms.Form):
    name = forms.CharField(label='Number', max_length=15)
