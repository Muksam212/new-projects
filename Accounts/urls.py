from django.urls import path
from accounts.views import RegisterView,LoginView, LogoutView


app_name = "accounts"

urlpatterns = [
	path('registerPage/', RegisterView.as_view(), name='register'),
	path('loginPage/', LoginView.as_view(), name='login'),
	path('logoutPage/', LogoutView.as_view(), name='logout')
]