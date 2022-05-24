from django.views.generic import *
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages

from news.views import UserRequiredMixin
from accounts.forms import RegisterForms, LoginForm

# Create your views here.
#register 

class RegisterView(SuccessMessageMixin,CreateView):
	template_name = 'register/register.html'
	form_class = RegisterForms
	success_url = reverse_lazy('accounts:register')
	success_message = "Your Information is Created"

	def form_valid(self, form):
		username=form.cleaned_data['username']
		password = form.cleaned_data['password1']
		cf_password =form.cleaned_data['password2']
		email = form.cleaned_data['email']



		if password == cf_password:
			if User.objects.filter(username=username).exists():
				messages.info(request, 'username is already exists')
			elif User.objects.filter(email = email ).exists():
				messages.info(request, 'email is already exists')
		else:
			return render(self.request, self.template_name,
			{'error':'Invalid username or password','form':form})

		return super().form_valid(form)
	

	def get_success_message(self, cleaned_data):
		return self.success_message % cleaned_data

#for login
class LoginPage(FormView):
	template_name='registration/login.html'
	success_url=reverse_lazy('news:dashboard-page')
	form_class=LoginForm

	def form_valid(self, form):
		uname=form.cleaned_data['username']
		pword=form.cleaned_data['password']
		user = authenticate(username=uname, password=pword)
		
		if user is not None:
			login(self.request, user)
		else:
			return render(self.request,'registration/login.html',
			{'Error':'Invalid username or password','form':form})

		return super().form_valid(form)