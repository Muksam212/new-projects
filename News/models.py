from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField
from embed_video.fields import EmbedVideoField
#create your models here


class Category(models.Model):
	title = models.CharField(max_length=100)
	parent = models.ForeignKey('self', related_name='parents', null=True, blank=True, on_delete=models.CASCADE)

	class Meta:
		verbose_name='Category'
		verbose_name_plural='Categories'

	def __str__(self):
		return self.title

class Author(models.Model):
	name = models.CharField(max_length=100, blank=False)
	address = models.CharField(max_length=100)
	email = models.EmailField()
	image = models.ImageField(upload_to='author/images')

	class Meta:
		verbose_name='Author'
		verbose_name_plural='Authors'

	def __str__(self):
		return "{}".format(self.name)

	def get_absolute_url(self):
		return reverse("News:create-author", kwargs={'id':self.id})


class New(models.Model):
	category=models.ForeignKey(Category, on_delete=models.CASCADE)
	subcategory=models.ManyToManyField(Category, related_name='news')
	title=models.CharField(max_length=100)
	image=models.ImageField(upload_to='news/imgs')
	bannerimage=models.ImageField(upload_to='add/images')
	details=RichTextField()

	class Meta:
		verbose_name='New'
		verbose_name_plural='News'

	def __str__(self):
		return "{} -> {}".format(self.category, self.title)


class Comment(models.Model):
	author=models.ForeignKey(Author, on_delete=models.CASCADE)
	news=models.ForeignKey(New, on_delete=models.CASCADE)
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	email=models.CharField(max_length=100)
	comment=RichTextField()
	status=models.BooleanField(default=False)

	class Meta:
		verbose_name='Comment'
		verbose_name_plural='Comments'

	def __str__(self):
		return str(self.user)


class Video(models.Model):
	title=models.CharField(max_length=100)
	url=EmbedVideoField()
	date_created=models.DateField() 

	class Meta:
		verbose_name='Video'
		verbose_name_plural='Videos'

	def __str__(self):
		return "{}".format(self.title)