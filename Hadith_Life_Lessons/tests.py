from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Hadith_Life_Lessons


class HadithLifeLessonsApiTests(APITestCase):
    def setUp(self):
        self.lesson = Hadith_Life_Lessons.objects.create(
            hadithLessonName="সুন্দর আচরণের শিক্ষা",
            hadithLessonDescription="হাদিস থেকে পাওয়া একটি জীবনঘনিষ্ঠ শিক্ষা।",
        )

    def test_lists_hadith_life_lessons(self):
        response = self.client.get(reverse("hadith-life-lessons-list-create"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["hadithLessonName"],
            self.lesson.hadithLessonName,
        )

    def test_retrieves_a_hadith_life_lesson(self):
        response = self.client.get(
            reverse(
                "hadith-life-lessons-retrieve-update-destroy",
                kwargs={"id": self.lesson.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.lesson.id))

