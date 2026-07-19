from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Life_Lessons


class LifeLessonsApiTests(APITestCase):
    def setUp(self):
        self.lesson = Life_Lessons.objects.create(
            lifeLessonName="অভিজ্ঞতা থেকে শেখা",
            lifeLessonDescription="জীবনের অভিজ্ঞতা থেকে পাওয়া একটি শিক্ষা।",
        )

    def test_lists_life_lessons(self):
        response = self.client.get(reverse("life-lessons-list-create"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["lifeLessonName"],
            self.lesson.lifeLessonName,
        )

    def test_retrieves_a_life_lesson(self):
        response = self.client.get(
            reverse(
                "life-lessons-retrieve-update-destroy",
                kwargs={"id": self.lesson.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.lesson.id))

