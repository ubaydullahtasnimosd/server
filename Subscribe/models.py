from django.db import models
import uuid 
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

class Subscriber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1000, verbose_name='যে সাবস্ক্রাইব করবে তার নাম')
    email = models.EmailField(unique=True, verbose_name='যে সাবস্ক্রাইব করবে তার ইমেইল')
    is_verified = models.BooleanField(default=False)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    verification_token = models.CharField(max_length=36, blank=True)   

    def __str__(self):
        return f'{self.name} - {self.email}'
    
    def send_verification_email(self, *args, **kwargs):
        verification_link = f'{settings.BASE_URL}/api/v1/subscribe/subscribe/verify/{self.verification_token}/'
        subject = 'আপনার সাবস্ক্রিপশন নিশ্চিত করুন'
        html_message = render_to_string('verification_email.html',{
            'name': self.name,
            'verification_link': verification_link,
        })
        plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            [self.email],
            html_message=html_message,
        )

    def send_welcome_email(self, *args, **kwargs):
        subject = 'সাবস্ক্রিপশন সফলভাবে সম্পন্ন হয়েছে!'
        html_message = render_to_string('welcome_email.html',{
            'name': self.name,
        })
        plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            [self.email],
            html_message=html_message,
        )

    class Meta:
        verbose_name_plural = 'সাবস্ক্রাইবার'


