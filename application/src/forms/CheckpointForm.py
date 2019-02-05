from django import forms


class CheckpointForm(forms.Form):
    name = forms.CharField(label='Name', max_length=63)
