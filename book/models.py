from django.db import models
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
    
    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new:
            self.send_new_book_notification()


    def send_new_book_notification(self, *args, **kwargs):
        from Subscribe.models import Subscriber 
        subscribers = Subscriber.objects.filter(is_verified=True)
        
        for subscriber in subscribers:
            try:
                subject = f"নতুন বই যোগ হয়েছে : {self.bookTitle}"
                html_message = render_to_string('new_book_notification.html', {
                    'subscriber': subscriber,
                    'book': self,
                    'base_url': settings.BASE_URL,
                })
                plain_message = strip_tags(html_message)
                
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[subscriber.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                print(f"ইমেইল পাঠানো হয়েছে: {subscriber.email}") 
            except Exception as e:
                print(f"ইমেইল পাঠাতে ব্যর্থ: {subscriber.email}, এরর: {str(e)}")  

    class Meta:
        verbose_name_plural = 'লেখকের বইগুলো'