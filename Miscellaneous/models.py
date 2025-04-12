from django.db import models

class Misecllaneous(models.Model):
    misecllaneousTitle = models.CharField(max_length=2000, verbose_name='বিবিধ এর ভিডিওটির একটি টাইটেল লিখুন')
    misecllaneousVideo = models.CharField(max_length=2000, verbose_name='বিবিধ এর ভিডিও লিংক')
    misecllaneousCreateAt = models.DateTimeField(auto_now_add=True, verbose_name='বিবিধ ভিডিও আপলোড করার তারিখ')

    def __str__(self):
       return f'{self.misecllaneousTitle}'

    class Meta:
        verbose_name_plural = 'বিবিধ'