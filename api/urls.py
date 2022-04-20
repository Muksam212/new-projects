from django.urls import path
from api.views import AuthorList, AuthorDetails, CommentList, NewsList, CategoryList
from api import views


app_name="api"

urlpatterns=[
    path('api/author/', AuthorList.as_view(), name='author-list'),
    path('api/<int:id>/author/',AuthorDetails.as_view(), name='author-details'),

    path('api/comment/', CommentList.as_view(), name='comment-list'),
    path('api/<int:id>/comment/', CommentList.as_view(), name='comment-details'),

    path('api/news/', NewsList.as_view(), name='new-list'),
    path('api/<int:id>/news/', NewsList.as_view(), name='new-details'),

    path('api/category/', CategoryList.as_view(), name='category-list'),
    path('api/<int:id>/category/', CategoryList.as_view(), name='category-details')
    
]