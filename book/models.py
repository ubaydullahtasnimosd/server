from django.db import models
import uuid

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bookImage = models.CharField(max_length=2000, verbose_name='লেখকের বইয়ের ছবির লিংক দিন')
    bookTitle = models.CharField(max_length=1000, verbose_name='লেখকের বইয়ের নাম')
    bookPublication = models.CharField(max_length=1000, verbose_name='লেখকের বইয়ের প্রকাশনা')
    bookDescription = models.TextField(verbose_name='লেখকের বইয়ের বিস্তারিত লেখা')
    bookPurchaseLink = models.CharField(max_length=2000, verbose_name='এখানে বইয়ের ক্রয়ের লিংক')
    bookCreatedAt = models.DateTimeField(auto_now_add=True, verbose_name='ওয়েবসাইটে বই প্রকাশের তারিখ')
    bookUpdateAt = models.DateTimeField(auto_now=True, verbose_name='বইয়ের লেখা ইডিট এর তারিখ')

    def __str__(self):
        return f'{self.bookTitle}'
    
    class Meta:
        verbose_name_plural = 'লেখকের বইগুলো'