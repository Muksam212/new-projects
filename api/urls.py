from django.urls import path
from api.views import AuthorList, AuthorDetails, CommentList,CommentDetails, NewsList, NewDetails,CategoryList, CategoryDetails, VideoList, VideoDetails
from api import views


app_name="api"

urlpatterns=[
    path('api/author/', AuthorList.as_view(), name='author-list'),
    path('api/<int:id>/author/',AuthorDetails.as_view(), name='author-details'),

    path('api/comment/', CommentList.as_view(), name='comment-list'),
    path('api/<int:id>/comment/', CommentDetails.as_view(), name='comment-details'),

    path('api/news/', NewsList.as_view(), name='new-list'),
    path('api/<int:id>/news/', NewDetails.as_view(), name='new-details'),

    path('api/category/', CategoryList.as_view(), name='category-list'),
    path('api/<int:id>/category/', CategoryDetails.as_view(), name='category-details'),

    path('api/video/', VideoList.as_view(), name='video-list'),
    path('api/<int:id>/video/', VideoDetails.as_view(), name='video-details')

]