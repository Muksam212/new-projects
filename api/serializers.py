from rest_framework import serializers
from news.models import Author, Comment, Category, News, Video

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model=News
        fields=['id','author','category','title','image','details','subcategory']
        depth=1


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields=['id','news','address','email','image']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['id','author','news','user','email','comment','status']
        depth=1


class CategorySerializer(serializers.ModelSerializer):
    #implementation of nested serializer
    subcategory_news = NewsSerializer(many=True, read_only=True)
    class Meta:
        model=Category
        fields=['id','subcategory_news']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Video
        fields=['id','title','url','date_created']