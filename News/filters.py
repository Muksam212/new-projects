# from attr import field
from cgitb import lookup
from turtle import title
from unicodedata import category

import django_filters 
from .models import Author, Comment, News, Category

class AuthorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr = 'iexact')

    class meta:
        model = Author
        fields = ('name')

class NewsFilter(django_filters.FilterSet):    

    class Meta:
        model = News
        fields = {
            'title' : ['icontains'],
            'category__title' : ['icontains']
        }

class CategoryFilter(django_filters.FilterSet):
    title= django_filters.CharFilter(lookup_expr = 'iexact')

    class meta:
        model = Category
        fields = ('title')
