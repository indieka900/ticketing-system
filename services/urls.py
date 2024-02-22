from django.urls import path
from services.views import (
    home
)

app_name = 'services'

urlpatterns = [
    path('', home, name='homepage'),
]