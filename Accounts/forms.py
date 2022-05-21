from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

class SignUpForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput())
	email = forms.CharField(widget=forms.EmailInput())
	pword = forms.CharField(widget=forms.PasswordInput())
	cf_pword = forms.CharField(widget=forms.PasswordInput())

	def clean(self):
		uname = self.cleaned_data['username']
		if User.objects.filter(username=uname).exists():
			raise forms.ValidationError("Username Aleady exists. Please take another username")

	def check_password(self):
		if pword != cf_pword:
			raise format.ValidationError("Password didn't match")

class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder':'Enter your username.',
		'class':'form-control',
		}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder':'Enter your password',
		'class':'form-control',
		}))
