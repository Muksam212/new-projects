from pyexpat import model
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# from autoslug import AutoSlugField


#create your models here


class Category(models.Model):
	title = models.CharField(max_length=100)
	def __str__(self):
		return self.title

class Author(models.Model):
	name = models.CharField(max_length=100, blank=False)
	address = models.CharField(max_length=100)
	email = models.EmailField()
	image = models.ImageField(upload_to='author/images')


	def __str__(self):
		return "{}".format(self.name)

	def get_absolute_url(self):
		return reverse("News:create-author", kwargs={'id':self.id})


class News(models.Model):
	category=models.ForeignKey(Category, on_delete=models.CASCADE)
	# subcategory=models.ManyToManyField(Category, related_name='categorys')
	author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
	title=models.CharField(max_length=100)
	image=models.ImageField(upload_to='news/imgs')
	# banneradd=models.ImageField(upload_to='bannersadd/images')
	# slug = AutoSlugField(populate_from = 'title', unique = True, null = True, default = None)
	details=RichTextField()

	class Meta:
		verbose_name = "News"
		verbose_name_plural = "News"

	def __str__(self):
		return "{} -> {}".format(self.category, self.title)


class Comment(models.Model):
	author=models.ForeignKey(Author, on_delete=models.CASCADE)
	news=models.ForeignKey(News, on_delete=models.CASCADE)
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	email=models.CharField(max_length=100)
	comment=RichTextField()
	status=models.BooleanField(default=False)

	def __str__(self):
		return str(self.user)


class Video(models.Model):
	title = models.CharField(max_length=100)
	video_link = models.URLField(max_length=200)
	thumbnail = models.ImageField(upload_to='video/images')

	def __str__(self):
		return "{}".format(self.title)

class Banneradd(models.Model):
	title = models.CharField(max_length=50)
	image = models.ImageField(upload_to = 'banneradd/image')
	url=models.URLField(max_length=255)
	is_active=models.BooleanField(default=False)

	def __str__(self):
		return "{}".format(self.title)




