from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

class SignUpForm(UserCreationForm):
	class Meta:
		model=User
		fields=['username','email','password1','password2']

class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder':'Enter your username.',
		'class':'form-control',
		}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder':'Enter your password',
		'class':'form-control',
		}))
