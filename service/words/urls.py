from .views import *
from django.urls import path

urlpatterns = [
    path('create_verbform/', CreateVerbFormsView.as_view()),
    path('list_verbform/', ListVerbFormsView.as_view()),
    # path('testing_view/', TestingView.as_view())
]
