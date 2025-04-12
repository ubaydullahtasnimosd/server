from django.shortcuts import render
from rest_framework import generics
from .models import AboutAuthor
from .serializers import AboutAuthorSerializers

class AboutAuthorApiView(generics.ListCreateAPIView):
    queryset = AboutAuthor.objects.all()
    serializer_class = AboutAuthorSerializers