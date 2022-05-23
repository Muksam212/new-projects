"""newproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from api.views import RegistrationAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('news.urls')),
    path('', include('newsapp.urls')),
    path('', include('api.urls')),

    path('api/register/', RegistrationAPIView.as_view(), name='auth-register'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/refresh-token/', TokenRefreshView.as_view(), name='refreshtoken'),


    #for reset password
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password-reset.html'), 
    name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password-reset-done.html'),
    name='password_reset_done'),


    path('password-reset-confirm/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(template_name='users/password-reset-confirm.html'),
    name='password_reset_confirm'),


    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(
    template_name='users/password-reset-complete.html'),
    name='password_reset_complete'),

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)