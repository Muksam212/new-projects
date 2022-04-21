from django.urls import path
from newsapp.views import BaseTemplate, DetailsTemplate, IndexTemplate

app_name='newsapp'

urlpatterns=[
    path('', IndexTemplate.as_view(), name = 'index'),
    path('category/<int:pk>/news', DetailsTemplate.as_view(), name='details-page'),
    

    
]