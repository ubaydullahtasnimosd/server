import uuid

from django.db import models

from Comment.models import Comment


class Hadith_Life_Lessons(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hadithLessonImg = models.CharField(
        max_length=3000,
        default="",
        null=True,
        blank=True,
        verbose_name="ছবি ইউআরএল",
    )
    hadithLessonName = models.CharField(
        max_length=1000,
        verbose_name="পাঠের শিরোনাম",
    )
    hadithLessonAuthor = models.CharField(
        max_length=300,
        default="উবায়দুল্লাহ তাসনিম",
        verbose_name="লেখকের নাম",
    )
    hadithLessonDescription = models.TextField(
        verbose_name="বিস্তারিত তথ্য",
        blank=True,
        null=True,
    )
    hadithLessonCreateAt = models.DateTimeField(
        auto_now_add=True,
        verbose_name="প্রকাশের তারিখ",
    )
    hadithLessonUpdateAt = models.DateTimeField(
        auto_now=True,
        verbose_name="সম্পাদনার তারিখ",
    )

    def __str__(self):
        return self.hadithLessonName

    @property
    def comments(self):
        return Comment.objects.filter(
            content_type__model="hadith_life_lessons",
            object_id=self.id,
        )

    class Meta:
        ordering = ["-hadithLessonCreateAt"]
        verbose_name_plural = "হাদিস থেকে জীবনের পাঠ"

