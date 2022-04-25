from django.views.generic import *
from django.views import View
from .forms import RegisterForms, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from news.views import LoginRequiredMixin

from django.views.generic import RedirectView

# Create your views here.
#register 

class RegisterView(SuccessMessageMixin,CreateView):
	template_name = 'register/register.html'
	form_class = RegisterForms
	success_url = reverse_lazy('accounts:register')
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
	success_url=reverse_lazy('news:dashboard-page')
	form_class=LoginForm

	def form_valid(self, form):
		uname = form.cleaned_data['username']
		pword = form.cleaned_data['password']

		usr = authenticate(username = uname, password = pword)
		if usr is not None:
			login(self.request, usr)
		else:
			return render(self.request, self.template_name, {
					'error':'Invalid username or password',
					'form':form
				})

		return super().form_valid(form)

class LogoutView(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		return redirect('accounts:login')