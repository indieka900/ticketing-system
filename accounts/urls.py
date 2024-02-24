from django.urls import path
from django.contrib.auth import views as view
from accounts.views import (
    SignupView, login_user, changePassword
)

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='sign-up'),
    path('logout/', view.LogoutView.as_view(), name='logout'),
    path('signin/', login_user, name='login'),
]
