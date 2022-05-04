from django.contrib import admin
from .models import Author, Category, News, Comment
# Register your models here.
# admin.site.register([Author,Category,News,Comment])

# class NewsAdmin(admin.ModelAdmin):
#     list_display=['slug','title']

# admin.site.register(News,NewsAdmin)