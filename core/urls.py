from django.urls import path
from .views import *

urlpatterns = [
    path('message/', CreateMessage.as_view()),
    path('active/', ActiveHospital.as_view()),
    path('message/<str:pk>/', HospitalMessageView.as_view())
]