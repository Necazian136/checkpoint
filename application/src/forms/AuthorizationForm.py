from django import forms


class AuthorizationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)
