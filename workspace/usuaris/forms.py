from django import forms
from django.contrib.auth.models import User

class Login_form(forms.Form):
    username = forms.CharField(max_length=100);
    password = forms.CharField(widget=forms.PasswordInput)
    
class Signup_form(forms.Form):
    username = forms.CharField(max_length=100);
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Aquest nom d\'usuari ja esta registrat')
        return username