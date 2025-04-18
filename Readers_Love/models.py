from django.db import models

class Readers_Love(models.Model):
    readersBookImg = models.CharField(max_length=2000, default='', verbose_name='রিভিউকৃত বইয়ের ছবি')
    readersBookName = models.CharField(max_length=1000, verbose_name='রিভিউকৃত বইয়ের নাম')
    readersName = models.CharField(max_length=1000, verbose_name='পাঠকের নাম')
    readersReview = models.TextField(verbose_name='রিভিউ সম্পর্কে বিস্তারিত') 
    readersReviewCreated = models.DateTimeField(auto_now_add=True, verbose_name='রিভিয়ের তারিখ')

    def __str__(self):
        return f'{self.readersName} - {self.readersBookName}'
    
    class Meta:
        verbose_name_plural = 'পাঠকের ভালোবাসা'
        
class Readers_Love_Img(models.Model):
    readersBookImg = models.CharField(max_length=2000, default='', verbose_name='রিভিউকৃত বইয়ের ছবি')
    readersReviewCreated = models.DateTimeField(auto_now_add=True, verbose_name='রিভিয়ের তারিখ')

    def __str__(self):
        return f'{self.readersBookImg}'
    
    class Meta:
        verbose_name_plural = 'পাঠকের ভালোবাসা | বইয়ের কভারসমূহ'