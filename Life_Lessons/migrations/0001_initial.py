import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Life_Lessons",
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
                    "lifeLessonImg",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=3000,
                        null=True,
                        verbose_name="ছবি ইউআরএল",
                    ),
                ),
                (
                    "lifeLessonName",
                    models.CharField(
                        max_length=1000,
                        verbose_name="শিক্ষার শিরোনাম",
                    ),
                ),
                (
                    "lifeLessonAuthor",
                    models.CharField(
                        default="উবায়দুল্লাহ তাসনিম",
                        max_length=300,
                        verbose_name="লেখকের নাম",
                    ),
                ),
                (
                    "lifeLessonDescription",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="বিস্তারিত তথ্য",
                    ),
                ),
                (
                    "lifeLessonCreateAt",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="প্রকাশের তারিখ",
                    ),
                ),
                (
                    "lifeLessonUpdateAt",
                    models.DateTimeField(
                        auto_now=True,
                        verbose_name="সম্পাদনার তারিখ",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "জীবন থেকে নেওয়া শিক্ষা",
                "ordering": ["-lifeLessonCreateAt"],
            },
        ),
    ]

