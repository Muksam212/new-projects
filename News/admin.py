from django.contrib import admin
from .models import Author, Category, News, Comment, Video
# Register your models here.

admin.site.register([Author,Category,News,Comment,Video])
