from django.urls import path
from News.views import (CommentList,CommentCreate, CommentUpdate, IndexView,AuthorList, AuthorUpdate, 
CategoryUpdate, AuthorCreate,DashboardTemplate,
AuthorList,AuthorUpdate, AuthorDelete,NewsCreate,NewList, NewsUpdate, NewsDelete, CategoryCreate, 
CategoryList,CategoryUpdate,CategoryDelete,)


app_name ='News' #implementing custom url

urlpatterns = [
    path('index/',IndexView.as_view(),name='index'),
    path('dashboard/', DashboardTemplate.as_view(), name='dashboard-page'),
    
    #author crud
    path('createAuthor/',AuthorCreate.as_view(), name='create-author'),
    path('listAuthor/', AuthorList.as_view(), name='list-author'),
    path('author/<int:id>/update/', AuthorUpdate.as_view(), name='update-author'),
    path('author/<int:id>/delete/', AuthorDelete.as_view(), name='delete-author'),
    
    #news
    path('newslist/', NewList.as_view(), name='new-list'),
    path('createNews/', NewsCreate.as_view(), name='create-news'),
    path('news/<int:id>/update/',NewsUpdate.as_view(), name='update-news'),
    path('news/<int:id>/delete/',NewsDelete.as_view(), name='delete-news'),

    #category
    path('categoryList/', CategoryList.as_view(), name='category-list'),
    path('createCategory/', CategoryCreate.as_view(), name='create-category'),
    path('category/<int:id>/update/',CategoryUpdate.as_view(), name='update-category'),
    path('category/<int:id>/delete/', CategoryDelete.as_view(), name='delete-category'),

    #comment
    path('commentList/', CommentList.as_view(), name='comment-list'),
    path('commentCreate/', CommentCreate.as_view(), name='comment-create'),
    path('comment/<int:id>/update/', CommentUpdate.as_view(), name='comment-update')
]
