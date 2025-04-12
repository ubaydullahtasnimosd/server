from django.db import models
import uuid

class Articles_Essays(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4 , editable=False)
    articlesEssaysName = models.CharField(max_length=1000, verbose_name='প্রবন্ধ-নিবন্ধর নাম')
    articlesEssaysAuthor = models.CharField(max_length=300, verbose_name='প্রবন্ধ-নিবন্ধর লেখকের নাম')
    articlesEssaysDescription = models.TextField(verbose_name='প্রবন্ধ-নিবন্ধ সম্পর্কে বিস্তারিত', blank=True, null=True)
    articlesEssaysQRCodeScen = models.TextField(verbose_name='প্রবন্ধ-নিবন্ধর প্রকাশনা এবং স্ক্যান করা')
    articlesEssaysCreateAt = models.DateTimeField(auto_now_add=True, verbose_name='ওয়েবসাইটে প্রবন্ধ-নিবন্ধ প্রকাশের তারিখ')
    articlesEssaysUpdateAt = models.DateTimeField(auto_now=True, verbose_name='প্রবন্ধ-নিবন্ধ লেখা ইডিট এর তারিখ')

    def __str__(self):
        return f'{self.articlesEssaysName}'
    
    class Meta:
        verbose_name_plural = 'প্রবন্ধ-নিবন্ধ'