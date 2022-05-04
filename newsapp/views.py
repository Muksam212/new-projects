from django.shortcuts import render, get_object_or_404
from django.views.generic import *
from django.urls import reverse_lazy


from news.models import Banneradd
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
    paginate_by = 1
    context_object_name = 'news_detail'

    def get_queryset(self):
        queryset =  super().get_queryset()
        pk = self.kwargs['pk']
        return queryset.filter(category__id=pk)
    
    def get_category(self):
        category_id = self.kwargs.get('pk')
        category = Category.objects.get(id=category_id)
        return category
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['category_object'] = Category.objects.filter(id=pk).last()
        context['category_news'] = News.objects.filter(category= self.get_category()).order_by('-id')
        return context
        

class IndexTemplate(BaseMixin, TemplateView):
    template_name='index.html'
    sucess_url = reverse_lazy('newsapp:index')
    model=News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_news'] = News.objects.all().order_by('-id')
        context['sports_news'] = News.objects.filter(category__title='खेलकुद').order_by('-id')
        context['political_news'] =News.objects.filter(category__title = 'राजनीति').order_by('-id')[:1]
        context['business_news'] = News.objects.filter(category__title = 'अर्थ').order_by('-id')[:1]
        context['cinema_news'] = News.objects.filter(category__title = 'सिनेमा').order_by('-id')[:1]
        context['banner_add'] = Banneradd.objects.filter(is_active=True).order_by('-id')[:1]
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