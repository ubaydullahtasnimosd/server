import uuid

from django.db import migrations, models


def content_fields():
    return [
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
            "contentImg",
            models.CharField(
                blank=True,
                default="",
                max_length=3000,
                null=True,
                verbose_name="ছবি ইউআরএল",
            ),
        ),
        (
            "contentName",
            models.CharField(max_length=1000, verbose_name="পাঠের শিরোনাম"),
        ),
        (
            "contentAuthor",
            models.CharField(
                default="উবায়দুল্লাহ তাসনিম",
                max_length=300,
                verbose_name="লেখকের নাম",
            ),
        ),
        (
            "contentDescription",
            models.TextField(blank=True, null=True, verbose_name="বিস্তারিত তথ্য"),
        ),
        (
            "contentCreateAt",
            models.DateTimeField(auto_now_add=True, verbose_name="প্রকাশের তারিখ"),
        ),
        (
            "contentUpdateAt",
            models.DateTimeField(auto_now=True, verbose_name="সম্পাদনার তারিখ"),
        ),
    ]


def content_model(name, verbose_name_plural):
    return migrations.CreateModel(
        name=name,
        fields=content_fields(),
        options={
            "verbose_name_plural": verbose_name_plural,
            "ordering": ["-contentCreateAt"],
        },
    )


class Migration(migrations.Migration):
    dependencies = [("Miscellaneous", "0001_initial")]

    operations = [
        content_model("Culture", "কালচার, সংস্কৃতি"),
        content_model("Travel", "ভ্রমণ"),
        content_model("History", "ইতিহাস"),
        content_model("Politics", "রাজনীতি"),
        content_model("Worldview", "বিশ্ব-দর্শন"),
    ]
