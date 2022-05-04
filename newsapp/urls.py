from django.urls import path
from newsapp.views import BaseTemplate, DetailsTemplate, IndexTemplate, DetailnewsView
from django.contrib.auth import views as auth_views

app_name='newsapp'

urlpatterns=[
    path('', IndexTemplate.as_view(), name = 'index'),
    path('category/<int:pk>/', DetailsTemplate.as_view(), name='details-page'),
    path('details/<int:pk>/news/', DetailnewsView.as_view(), name ='detail-news'),
]
    

    
