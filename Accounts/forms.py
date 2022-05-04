from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

class RegisterForms(UserCreationForm):
	class Meta:
		model = User
		fields=['username','email','password1','password2']

	def clean_username(self):
		uname=self.cleaned_data['username']
		if User.objects.filter(username=uname).exists():
			raise forms.ValidationError("Username already exists")
		return uname

	def clean(self):
		if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
			raise forms.ValidationError("Password are note equal")
		return self.cleaned_data


class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder':'Enter your username.',
		'class':'form-control',
		}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder':'Enter your password',
		'class':'form-control',
		}))
