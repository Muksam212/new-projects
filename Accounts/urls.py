from django.urls import path
from accounts.views import RegisterView,LoginPage


app_name = "accounts"

urlpatterns = [
	path('registerPage/', RegisterView.as_view(), name='register'),
	path('loginPage/', LoginPage.as_view(), name='login'),
]