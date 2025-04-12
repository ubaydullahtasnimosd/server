from django.db import models

class AboutAuthor(models.Model):
    aboutAuthorName = models.CharField(max_length=200, verbose_name='লেখকের নাম')
    aboutAuthorDescription = models.TextField(verbose_name='লেখক সম্পর্কে বিস্তারিত লিখুন')

    def __str__(self):
        return f'{self.aboutAuthorName}'
    
    class Meta:
        verbose_name_plural = 'লেখক সম্পর্কে'