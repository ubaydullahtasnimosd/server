import uuid

from django.db import models

from Comment.models import Comment


class Life_Lessons(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lifeLessonImg = models.CharField(
        max_length=3000,
        default="",
        null=True,
        blank=True,
        verbose_name="ছবি ইউআরএল",
    )
    lifeLessonName = models.CharField(
        max_length=1000,
        verbose_name="শিক্ষার শিরোনাম",
    )
    lifeLessonAuthor = models.CharField(
        max_length=300,
        default="উবায়দুল্লাহ তাসনিম",
        verbose_name="লেখকের নাম",
    )
    lifeLessonDescription = models.TextField(
        verbose_name="বিস্তারিত তথ্য",
        blank=True,
        null=True,
    )
    lifeLessonCreateAt = models.DateTimeField(
        auto_now_add=True,
        verbose_name="প্রকাশের তারিখ",
    )
    lifeLessonUpdateAt = models.DateTimeField(
        auto_now=True,
        verbose_name="সম্পাদনার তারিখ",
    )

    def __str__(self):
        return self.lifeLessonName

    @property
    def comments(self):
        return Comment.objects.filter(
            content_type__model="life_lessons",
            object_id=self.id,
        )

    class Meta:
        ordering = ["-lifeLessonCreateAt"]
        verbose_name_plural = "জীবন থেকে নেওয়া শিক্ষা"

