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
class LoginPage(FormView):
	template_name='registration/login.html'
	success_url=reverse_lazy('News:dashboard-page')
	form_class=LoginForm

	def form_valid(self, form):
		uname=form.cleaned_data['username']
		print(uname,'---------')
		pword=form.cleaned_data['password']
		print(pword,'----------')

		user = authenticate(username=uname, password=pword)
		print(user, '=====================')
		if user is not None:
			print(user, '---------------------')
			login(self.request, user)
		else:
			return render(self.request,'registration/login.html',
			{'Error':'Invalid username or password','form':form})

		return super().form_valid(form)


class LogoutView(View):
	def get(self, request):
		logout(request)
		return redirect("/loginPage")
class PasswordReset(TemplateView):
	template_name='registration/reset_password.html'