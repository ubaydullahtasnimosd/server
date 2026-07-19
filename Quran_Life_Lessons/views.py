from rest_framework import generics
from .models import Quran_Life_Lessons
from .serializers import QuranLifeLessonsSerializer

class QuranLifeLessonsListCreateView(generics.ListCreateAPIView):
    queryset = Quran_Life_Lessons.objects.all().order_by('-quranLessonCreateAt')
    serializer_class = QuranLifeLessonsSerializer
    
class QuranLifeLessonsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quran_Life_Lessons.objects.all()
    serializer_class = QuranLifeLessonsSerializer
    lookup_field = 'id'
