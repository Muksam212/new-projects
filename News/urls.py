from django.urls import path
from news.views import (CommentList,CommentCreate, CommentUpdate, CommentDelete, CommentDetailsPdf,
IndexView,AuthorList, AuthorUpdate, CommentDetailsCSV,CommentDetailsExcel,
CategoryUpdate, AuthorCreate,DashboardTemplate,ChartDetails,
AuthorList,AuthorUpdate, AuthorDelete,NewsCreate,NewList, NewsUpdate, NewsDelete, CategoryCreate, 
CategoryList,CategoryUpdate,CategoryDelete,AuthorDetailsPdf,AuthorDetailsCSV,AuthorDetailsExcel,NewsDetailsPdf,
NewsDetailsCSV,NewsDetailsExcel,CategoryDetailsPdf,CategoryDetailsCSV,CategoryDetailsExcel, ChartDetails,LogoutView)


app_name ='news' #implementing custom url

urlpatterns = [

    #for logout
    path('logoutPage/', LogoutView.as_view(), name='logout'),

    #for chart, dashboard
    path('chart/', ChartDetails.as_view(), name='chart-page'),
    path('index/',IndexView.as_view(),name='index'),
    path('dashboard/', DashboardTemplate.as_view(), name='dashboard-page'),
    path('chartDetails/', ChartDetails.as_view(),name='chart-details'),
    
    #author crud
    path('listAuthor/', AuthorList.as_view(), name='list-author'),
    path('createAuthor/',AuthorCreate.as_view(), name='create-author'),
    path('author/<int:id>/update/', AuthorUpdate.as_view(), name='update-author'),
    path('author/<int:id>/delete/', AuthorDelete.as_view(), name='delete-author'),
    path('authorPdf/', AuthorDetailsPdf.as_view(), name='author-pdf'),
    path('authorCsv/', AuthorDetailsCSV.as_view(), name='author-csv'),
    path('authorExcel/',AuthorDetailsExcel.as_view(), name='author-excel'),
    
    #news
    path('newslist/', NewList.as_view(), name='new-list'),
    path('createNews/', NewsCreate.as_view(), name='create-news'),
    path('news/<int:id>/update/',NewsUpdate.as_view(), name='update-news'),
    path('news/<int:id>/delete/',NewsDelete.as_view(), name='delete-news'),
    path('newPdf/',NewsDetailsPdf.as_view(), name='new-pdf'),
    path('newCsv/',NewsDetailsCSV.as_view(), name='new-csv'),
    path('newExcel/', NewsDetailsExcel.as_view(), name='new-excel'),

    #category
    path('categoryList/', CategoryList.as_view(), name='category-list'),
    path('createCategory/', CategoryCreate.as_view(), name='create-category'),
    path('category/<int:id>/update/',CategoryUpdate.as_view(), name='update-category'),
    path('category/<int:id>/delete/', CategoryDelete.as_view(), name='delete-category'),
    path('categoryPdf/',CategoryDetailsPdf.as_view(), name='category-pdf'),
    path('categoryCsv/',CategoryDetailsCSV.as_view(), name='category-csv'),
    path('categoryExcel/',CategoryDetailsExcel.as_view(), name='category-excel'),

    #comment
    path('commentList/', CommentList.as_view(), name='comment-list'),
    path('commentCreate/', CommentCreate.as_view(), name='comment-create'),
    path('comment/<int:id>/update/', CommentUpdate.as_view(), name='comment-update'),
    path('comment/<int:id>/delete/', CommentDelete.as_view(), name='comment-delete'),
    path('commentPdf/', CommentDetailsPdf.as_view(), name='comment-pdf'),
    path('commentCsv/', CommentDetailsCSV.as_view(), name='comment-csv'),
    path('commentExcel/', CommentDetailsExcel.as_view(), name='comment-excel'),

    #sub-category
]
