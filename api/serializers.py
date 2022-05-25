from rest_framework import serializers
from news.models import Author, Comment, Category, News, Video

from django.contrib.auth.models import User

#register serializers
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        fields = ('username','email','password')

    def validate(self, args):
        email = args.get('email', None)
        username = args.get('username', None)

        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError({'email':{'email already exists'}})
        if User.objects.filter(username = username).exists():
            raise serializers.ValidationError({'username':{'username already exists'}})

        return super().validate(args)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id','author','category','title','image','details','subcategory']
        depth = 1


class AuthorSerializer(serializers.ModelSerializer):
    #implementing nested serializer for author
    news = NewsSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['id','news','address','email','image']
        depth = 1 

class CommentSerializer(serializers.ModelSerializer):
    authors = NewsSerializer(many=True, read_only=True)
    class Meta:
        model = Comment
        fields = ['id','authors','news','user','email','comment','status']
        depth = 1


class CategorySerializer(serializers.ModelSerializer):
    #implementation of nested serializer
    subcategory_news = NewsSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id','subcategory_news']
        depth = 1


class VideoSerializer(serializers.ModelSerializer):
    videos = AuthorSerializer(many=True, read_only=True)
    class Meta:
        model = Video
        fields = ['id','videos','url','date_created']
        depth = 1