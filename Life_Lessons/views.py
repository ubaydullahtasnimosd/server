from rest_framework import generics

from .models import Life_Lessons
from .serializers import LifeLessonsSerializer


class LifeLessonsListCreateView(generics.ListCreateAPIView):
    queryset = Life_Lessons.objects.all()
    serializer_class = LifeLessonsSerializer


class LifeLessonsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Life_Lessons.objects.all()
    serializer_class = LifeLessonsSerializer
    lookup_field = "id"

