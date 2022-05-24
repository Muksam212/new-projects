from dataclasses import field
from django import forms
from django.contrib.auth.models import User

class RegisterForms(forms.ModelForm):
	username=forms.CharField(widget=forms.TextInput())
	password1 = forms.CharField(widget = forms.PasswordInput())
	password2 = forms.CharField(widget = forms.PasswordInput())
	email = forms.CharField(widget=forms.TextInput())

	class Meta:
			model = User
			fields=['username','password1','password2','email']
			

class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder':'Enter your username.',
		'class':'form-control',
		}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder':'Enter your password',
		'class':'form-control',
		}))