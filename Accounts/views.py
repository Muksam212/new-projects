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

	def get(self, request):
		form = self.form_class
		message =''
		return render(request, self.template_name, context={'form':form,'message':message})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			usr = authenticate(
				uname = request.POST['username'],
				pword = request.POST['pssword']
				)
			if usr is not None:
				login(request, usr)
				return redirect('news:dashboard-page')
		message='login failed'
		return render(request, self.template_name, context={'form':form, 'message':message})

class LogoutView(LoginRequiredMixin,RedirectView):
	
	def get_redirect_url(self, *args, **kwargs):
		if self.request.user.is_authenticated():
			logout(self, request)
		return super(LogoutView,self).get_redirect_url(*args, **kwargs)