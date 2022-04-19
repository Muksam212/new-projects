from re import template
from django.shortcuts import render
from django.views.generic import *
from django.urls import reverse_lazy
# Create your views here.

class BaseTemplate(TemplateView):
    template_name='base.html'
    success_url=reverse_lazy('newsapp:index-page')

class DetailsTemplate(TemplateView):
    template_name='details.html'
    success_url=reverse_lazy('newsapp:details-page')

class IndexTemplate(TemplateView):
    template_name='index.html'
    success_url = reverse_lazy('newsapp:index')
