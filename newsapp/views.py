from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.views.generic import *
from django.urls import reverse_lazy

from news.models import Category
from news.models import News
# Create your views here.

class BaseMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_news'] = News.objects.all()
        context['sports_news'] = News.objects.filter(category__title='खेलकुद')
        return context

    def today():
        today = datetime.datetime.now().strftime("%I")
