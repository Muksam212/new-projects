import django_filters
from news.models import Author, Category

class AuthorFilter(django_filters.FilterSet):
	name=django_filters.CharFilter(lookup_expr='icontains')

	class Meta:
		model = Author
		fields =['name']


class CategoryFilter(django_filters.FilterSet):
	class Meta:
		model = Category
		fields = ['title']
