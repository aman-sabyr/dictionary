from .views import *
from django.urls import path

urlpatterns = [
    path('create_verbform/', ListCreateVerbFormsView.as_view()),
    path('list_verbform/', ListCreateVerbFormsView.as_view())
]
