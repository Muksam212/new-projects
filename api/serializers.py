from rest_framework import serializers
from news.models import Author, Comment, Category, New, Video

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields=['id','name','address','email','image']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['id','author','news','user','email','comment','status']
        depth=1


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','title']


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model=New
        fields=['id','category','title','image','details','subcategory','bannerimage']
        depth=1


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Video
        fields=['id','title','url','date_created']