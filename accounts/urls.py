from django.urls import path
from django.contrib.auth import views as view
from accounts.views import (
    SignupView, login_user, changePassword,log_out
)

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='sign-up'),
    path('logout/', log_out, name='logout'),
    path('', login_user, name='login'),
]
