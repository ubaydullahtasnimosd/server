import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Hadith_Life_Lessons",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "hadithLessonImg",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=3000,
                        null=True,
                        verbose_name="ছবি ইউআরএল",
                    ),
                ),
                (
                    "hadithLessonName",
                    models.CharField(
                        max_length=1000,
                        verbose_name="পাঠের শিরোনাম",
                    ),
                ),
                (
                    "hadithLessonAuthor",
                    models.CharField(
                        default="উবায়দুল্লাহ তাসনিম",
                        max_length=300,
                        verbose_name="লেখকের নাম",
                    ),
                ),
                (
                    "hadithLessonDescription",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="বিস্তারিত তথ্য",
                    ),
                ),
                (
                    "hadithLessonCreateAt",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="প্রকাশের তারিখ",
                    ),
                ),
                (
                    "hadithLessonUpdateAt",
                    models.DateTimeField(
                        auto_now=True,
                        verbose_name="সম্পাদনার তারিখ",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "হাদিস থেকে জীবনের পাঠ",
                "ordering": ["-hadithLessonCreateAt"],
            },
        ),
    ]

