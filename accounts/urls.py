from django.urls import path
from accounts.views import (
    SignupView, login_user, changePassword
)

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='sign-up'),
    path('signin/', login_user, name='login'),
]
