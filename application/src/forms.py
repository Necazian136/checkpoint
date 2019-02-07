from django import forms


class AuthorizationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)


class CheckpointForm(forms.Form):
    name = forms.CharField(label='Name', max_length=63)


class PlateForm(forms.Form):
    name = forms.CharField(label='Number', max_length=15)
