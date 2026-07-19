from rest_framework import serializers
from .models import Quran_Life_Lessons

class QuranLifeLessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quran_Life_Lessons
        fields = [
            'id', 
            'quranLessonImg', 
            'quranLessonName', 
            'quranLessonAuthor', 
            'quranLessonDescription', 
            'quranLessonCreateAt', 
            'quranLessonUpdateAt'
        ]
