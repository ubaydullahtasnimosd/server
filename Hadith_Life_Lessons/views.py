from rest_framework import generics

from .models import Hadith_Life_Lessons
from .serializers import HadithLifeLessonsSerializer


class HadithLifeLessonsListCreateView(generics.ListCreateAPIView):
    queryset = Hadith_Life_Lessons.objects.all()
    serializer_class = HadithLifeLessonsSerializer


class HadithLifeLessonsRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Hadith_Life_Lessons.objects.all()
    serializer_class = HadithLifeLessonsSerializer
    lookup_field = "id"

