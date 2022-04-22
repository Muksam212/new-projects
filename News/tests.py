from django.test import TestCase
from .models import Author
# Create your tests here.

class TestDate(TestCase):
	def setup(self):
		author=Author.object.create(name='laxmi',address='manglabare',email='laxmilimbu10@gmail.com')

	def test_data(self):
		author = Author.objects.get(name="laxmi")
		self.assertEqual(author.name,"laxmi")
