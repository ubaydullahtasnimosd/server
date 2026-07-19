from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Culture, History, Politics, Travel, Worldview


class MiscellaneousContentApiTests(APITestCase):
    categories = (
        ("culture", Culture),
        ("travel", Travel),
        ("history", History),
        ("politics", Politics),
        ("worldview", Worldview),
    )

    def test_each_category_lists_its_content(self):
        for slug, model in self.categories:
            with self.subTest(category=slug):
                lesson = model.objects.create(
                    contentName=f"{slug} পাঠ",
                    contentDescription="বিস্তারিত তথ্য",
                )

                response = self.client.get(reverse(f"{slug}-list-create"))

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(len(response.data), 1)
                self.assertEqual(response.data[0]["id"], str(lesson.id))

    def test_each_category_retrieves_a_content_item(self):
        for slug, model in self.categories:
            with self.subTest(category=slug):
                lesson = model.objects.create(contentName=f"{slug} পাঠ")

                response = self.client.get(
                    reverse(f"{slug}-detail", kwargs={"id": lesson.id})
                )

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data["contentName"], lesson.contentName)
