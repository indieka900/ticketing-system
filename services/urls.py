from django.urls import path
from services.views import (
    home, view_complaint, view_feedbacks
)

app_name = 'services'

urlpatterns = [
    path('home/<str:type>/', home, name='homepage'),
    path('complaint/<str:pk>/', view_complaint, name='complaint'),
    path('feedbacks/<str:pk>/', view_feedbacks, name='feedbacks'),
]