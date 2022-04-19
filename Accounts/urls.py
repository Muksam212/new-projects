from django.urls import path
from Accounts.views import RegisterView,PasswordReset,LoginPage


app_name = "Accounts"

urlpatterns = [
	path('', RegisterView.as_view(), name='register'),
	path('login/', LoginPage.as_view(), name='login'),
	path('passwordReset/',PasswordReset.as_view(), name='reset')
]