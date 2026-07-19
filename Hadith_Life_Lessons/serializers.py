from rest_framework import serializers

from .models import Hadith_Life_Lessons


class HadithLifeLessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hadith_Life_Lessons
        fields = [
            "id",
            "hadithLessonImg",
            "hadithLessonName",
            "hadithLessonAuthor",
            "hadithLessonDescription",
            "hadithLessonCreateAt",
            "hadithLessonUpdateAt",
        ]
        read_only_fields = [
            "id",
            "hadithLessonCreateAt",
            "hadithLessonUpdateAt",
        ]

