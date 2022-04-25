from django.urls import path
from newsapp.views import BaseTemplate, DetailnewsView, DetailsTemplate, IndexTemplate

app_name='newsapp'

urlpatterns=[
    path('', IndexTemplate.as_view(), name = 'index'),
    path('category/<int:pk>/news/', DetailsTemplate.as_view(), name='details-page'),
    path('details/<int:pk>/news/', DetailnewsView.as_view(), name ='detail-news'),
]
    

    