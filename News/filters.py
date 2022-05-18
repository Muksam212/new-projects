import django_filters
from news.models import Author, Category, News

#similar to search query and this time using django_filters
class AuthorFilter(django_filters.FilterSet):
	name=django_filters.CharFilter(lookup_expr='icontains')

	class Meta:
		model = Author
		fields =['name']


class CategoryFilter(django_filters.FilterSet):
	class Meta:
		model = Category
		fields = ['title']

class NewsFilter(django_filters.FilterSet):
	#for foreign key in django filter
	author__name=django_filters.CharFilter(lookup_expr='icontains')
	subcategory__title = django_filters.CharFilter(lookup_expr = 'iexact')

	#to target the foreign key (underscore __) is used 
	class Meta:
		model = News
		fields = ['author__name', 'subcategory__title']