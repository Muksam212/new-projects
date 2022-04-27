from django.contrib import admin
from .models import Author, Category, New, Comment
# Register your models here.
admin.site.register([Author,Category,New,Comment])