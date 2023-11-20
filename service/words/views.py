from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .services_folder.find_verb import Something
from rest_framework.response import Response

from .models import VerbForm
from .serializers import *


class ListCreateVerbFormsView(generics.ListCreateAPIView):
    serializer_class = VerbFormSerializer
    models = VerbForm
    queryset = VerbForm.objects.all()


# class TestingView(APIView):
#     def get(self, request):
#         # smt = Something()
#         # print()
#         return Response(smt.do_smth(3, 45), 200)