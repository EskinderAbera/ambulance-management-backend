from django.urls import path
from .views import *

urlpatterns = [
    path('message/', CreateMessage.as_view()),
    path('create-driver/', CreateDriver.as_view()),
    path('active/', ActiveHospital.as_view()),
    path('message/<str:pk>/', HospitalMessageView.as_view()),
    path('login/', LoginView.as_view()),
    path('login-driver/', LoginViewDriver.as_view()),
    path('assign-message/', AssignMessage.as_view()),
    path('list-driver/<str:pk>/', ListDriver.as_view())
]