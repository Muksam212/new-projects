from multiprocessing import context
from unicodedata import category
from django.shortcuts import render, get_object_or_404
from django.views.generic import *
from django.urls import reverse_lazy
from requests import get

from News.models import News
# Create your views here.

class BaseTemplate(TemplateView):
    template_name='base.html'
    success_url=reverse_lazy('newsapp:index-page')

class DetailsTemplate(DetailView):
    template_name='details.html'
    success_url=reverse_lazy('newsapp:details-page')
    model = News
    context_object_name = 'news_detail'



class IndexTemplate(TemplateView):
    template_name='index.html'
<<<<<<< HEAD
    sucess_url = reverse_lazy('newsapp:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_qs = News.objects.all()
        # context['political_news'] = news_qs.filter(category__title='')
        # context['political_news'] = news_qs.filter(category__title='Business')
        # return context

    def get_context_data(self, **kwargs):
        category_qs = News.objects.all()
        context = super().get_context_data(**kwargs)
        context['business_news'] = category_qs.filter(category__title='अर्थ')
        context['political_news'] = category_qs.filter(category__title='राजनीति')

        return context 
    
=======
    success_url = reverse_lazy('newsapp:index')
>>>>>>> f9a27a9ef065607026a9dcac40798f1780bfc1ce
