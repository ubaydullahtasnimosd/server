from django.contrib import admin
from .models import Subscriber
import uuid

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_verified', 'subscribed_at']
    list_filter = ['is_verified', 'subscribed_at']
    search_fields = ['name', 'email']
    readonly_fields = ['subscribed_at', 'verification_token']
    list_editable = ['is_verified']
    actions = ['send_verification_email', 'send_welcome_email']

    def send_verification_email(self, request, queryset, *args, **kwargs):
        for subscriber in queryset:
            if not subscriber.is_verified:
                subscriber.send_verification_email()
        self.message_user(request, 'ভেরিফিকেশন ইমেইল পাঠানো হয়েছে')
    send_verification_email.short_description = 'ভেরিফিকেশন ইমেইল পাঠান'

    def send_welcome_email(self, request, queryset, *args, **kwargs):
        for subscriber in queryset.filter(is_verified=True):
            subscriber.send_welcome_email()
        self.message_user(request, 'স্বাগতম ইমেইল পাঠানো হয়েছে')
    send_welcome_email.short_description = 'স্বাগতম ইমেইল পাঠান'

    def save_model(self, request, obj, form, change):
        if not change and not obj.verification_token:
            obj.verification_token = str(uuid.uuid4())
            print(f"Generated token: {obj.verification_token}") 
        
        super().save_model(request, obj, form, change)
        
        if not change and not obj.is_verified:
            try:
                obj.send_verification_email()
                print(f"Email sent to {obj.email}")  
            except Exception as e:
                print(f"Error sending email: {str(e)}")  

admin.site.register(Subscriber, SubscriberAdmin)