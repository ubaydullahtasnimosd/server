import uuid

from django.db import models

from Comment.models import Comment

class Misecllaneous(models.Model):
    misecllaneousTitle = models.CharField(max_length=2000, verbose_name='বিবিধ এর ভিডিওটির একটি টাইটেল লিখুন')
    misecllaneousVideo = models.CharField(max_length=2000, verbose_name='বিবিধ এর ভিডিও লিংক')
    misecllaneousCreateAt = models.DateTimeField(auto_now_add=True, verbose_name='বিবিধ ভিডিও আপলোড করার তারিখ')

    def __str__(self):
       return f'{self.misecllaneousTitle}'

    class Meta:
        verbose_name_plural = 'বিবিধ'


class MiscellaneousContentBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contentImg = models.CharField(
        max_length=3000,
        default="",
        null=True,
        blank=True,
        verbose_name="ছবি ইউআরএল",
    )
    contentName = models.CharField(
        max_length=1000,
        verbose_name="পাঠের শিরোনাম",
    )
    contentAuthor = models.CharField(
        max_length=300,
        default="উবায়দুল্লাহ তাসনিম",
        verbose_name="লেখকের নাম",
    )
    contentDescription = models.TextField(
        blank=True,
        null=True,
        verbose_name="বিস্তারিত তথ্য",
    )
    contentCreateAt = models.DateTimeField(
        auto_now_add=True,
        verbose_name="প্রকাশের তারিখ",
    )
    contentUpdateAt = models.DateTimeField(
        auto_now=True,
        verbose_name="সম্পাদনার তারিখ",
    )

    def __str__(self):
        return self.contentName

    @property
    def comments(self):
        return Comment.objects.filter(
            content_type__model=self._meta.model_name,
            object_id=self.id,
        )

    class Meta:
        abstract = True
        ordering = ["-contentCreateAt"]


class Culture(MiscellaneousContentBase):
    class Meta(MiscellaneousContentBase.Meta):
        verbose_name_plural = "কালচার, সংস্কৃতি"


class Travel(MiscellaneousContentBase):
    class Meta(MiscellaneousContentBase.Meta):
        verbose_name_plural = "ভ্রমণ"


class History(MiscellaneousContentBase):
    class Meta(MiscellaneousContentBase.Meta):
        verbose_name_plural = "ইতিহাস"


class Politics(MiscellaneousContentBase):
    class Meta(MiscellaneousContentBase.Meta):
        verbose_name_plural = "রাজনীতি"


class Worldview(MiscellaneousContentBase):
    class Meta(MiscellaneousContentBase.Meta):
        verbose_name_plural = "বিশ্ব-দর্শন"
