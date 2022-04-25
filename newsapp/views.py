from datetime import datetime
from multiprocessing import context
from pyexpat import model
from unicodedata import category
from django.shortcuts import render, get_object_or_404
from django.views.generic import *
from django.urls import reverse_lazy
from news.models import Category,News   
# Create your views here.

class BaseMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news']=News.objects.all()
        # context['business_news'] = category_qs.filter(category__title='अर्थ')
        # context['political_news'] = category_qs.filter(category__title='राजनीति')
        # context['manoranjan_news'] = category_qs.filter(category__title ='मनोरन्जन')
        # context['sports_news']= category_qs.filter(category__title = 'खेलकुद')
        # context['bichar'] = category_qs.filter(category__title = 'बिचार')
        # context['cinema_news'] = category_qs.filter(category__title= 'सिनेमा')
 
        return context 
    

class BaseTemplate(TemplateView):
    template_name='base.html'
    success_url=reverse_lazy('newsapp:index-page')

class DetailsTemplate(BaseMixin, ListView):
    template_name='details.html'
    success_url=reverse_lazy('newsapp:details-page')
    model = News
    context_object_name = 'news_detail'
    paginate_by = 1

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        category = self.kwargs.get('pk')
        queryset = queryset.filter(category__id=category)
        return queryset
        

class IndexTemplate(BaseMixin, TemplateView):
    template_name='index.html'
    sucess_url = reverse_lazy('newsapp:index')
    model=News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_news'] = News.objects.all().order_by('-id')
        context['sports_news'] = News.objects.filter(category__title='खेलकुद').order_by('-id')
        return context

class DetailnewsView(BaseMixin, DetailView):
    ajax_template_name= 'detailnews_ajax.html'
    sucess_url = reverse_lazy('newsapp:detail-news') 
    model = News
    context_object_name = "newsdetail"

    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs)
        return context

    def get_template_names(self):
        return self.ajax_template_name