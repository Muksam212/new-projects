from django.urls import path
from Accounts.views import RegisterView,PasswordReset,LoginPage,LogoutView


app_name = "Accounts"

urlpatterns = [
	path('registerPage/', RegisterView.as_view(), name='register'),
	path('loginPage/', LoginPage.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('passwordReset/',PasswordReset.as_view(), name='reset')
]