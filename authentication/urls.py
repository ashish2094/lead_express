from django.urls import path 
from .views import RegistrationView, UsernameValidationView, EmailValidationView, LoginView, LogoutView, SetNewpassView, ResetpassView, AccountView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/', AccountView.as_view(), name='account'),
    path('reset-pass/', ResetpassView.as_view(), name='reset_pass'),
    path('setnew-pass/', SetNewpassView.as_view(), name='setnew_pass'),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()), name='validate_user'),
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()), name='validate_email'),
]