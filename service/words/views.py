from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .services_folder.find_verb import *
from rest_framework.response import Response
import json

from .models import VerbForm
from .serializers import *


class CreateVerbFormsView(APIView):
    def post(self, request):
        data = request.data
        serializer = CreateVerbFormsSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            verbForm = serializer.create(serializer.validated_data)
        return Response('everythin is pk', 200)


class ListVerbFormsView(generics.ListAPIView):
    model = VerbForm
    serializer_class = VerbFormSerializer
    queryset = VerbForm.objects.all()

