from django.views.generic import *
from django.views import View
from .forms import RegisterForms, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse

# Create your views here.
class HomeView(TemplateView):
	template_name ='main/home.html'
	success_url =reverse_lazy("Accounts:home")

#register 
class RegisterView(SuccessMessageMixin,CreateView):
	template_name = 'register/register.html'
	form_class = RegisterForms
	success_url = reverse_lazy('Accounts:register')
	success_message = "Your Information is Created"

	def form_valid(self, form):
		print(form.cleaned_data)
		return super().form_valid(form)

	def form_invalid(self, form):
		errors=form.errors.as_json()
		return JsonResponse({'errors':errors},status=400)

	def get_success_message(self, cleaned_data):
		return self.success_message % cleaned_data

#for login
class LoginView(FormView):
	template_name='registration/login.html'
	success_url=reverse_lazy('News:dashboard')
	form_class=LoginForm

	def form_valid(self, form):
		uname = form.cleaned_data['username']
		print(uname,"--------------")
		pword = form.cleaned_data['password']
		print(pword,"-----------")

		#this check the user and return the user otherwise 
		#None authenticate means just to check user
		#if there is no user it return None

		user = authenticate(username = uname, password = pword)

		if user is not None:
			login(self.request, user)
		else:
			return render(self.request,"registration/login.html",
				{'Error':'Invalid username or password','form':form})

		#super is to return form to super class
		return super().form_valid(form)

class LogoutView(View):
	def get(self, request):
		logout(request)
		return redirect("Accounts:login")


class PasswordReset(TemplateView):
	template_name='registration/reset_password.html'