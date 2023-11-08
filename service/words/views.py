from django.shortcuts import render
from rest_framework import generics

from .models import VerbForm
from .serializers import *


class ListCreateVerbFormsView(generics.ListCreateAPIView):
    serializer_class = VerbFormSerializer
    models = VerbForm
    queryset = VerbForm.objects.all()