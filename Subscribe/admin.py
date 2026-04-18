from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Subscriber
import uuid


@admin.register(Subscriber)
class SubscriberAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "is_verified",
        "subscribed_at",
    )

    search_fields = (
        "name",
        "email",
    )

    list_filter = (
        "is_verified",
        "subscribed_at",
    )

    ordering = ("-subscribed_at",)

    list_per_page = 20

    readonly_fields = (
        "subscribed_at",
        "verification_token",
    )

    list_editable = (
        "is_verified",
    )

    actions = (
        "send_verification_email",
        "send_welcome_email",
    )

    fieldsets = (
        ("Subscriber Information", {
            "fields": (
                "name",
                "email",
                "is_verified",
            )
        }),
        ("Verification", {
            "fields": (
                "verification_token",
            )
        }),
        ("Timestamp", {
            "fields": (
                "subscribed_at",
            )
        }),
    )

    def send_verification_email(self, request, queryset):
        sent_count = 0
        for subscriber in queryset:
            if not subscriber.is_verified:
                subscriber.send_verification_email()
                sent_count += 1
        self.message_user(request, f"{sent_count} জনের কাছে ভেরিফিকেশন ইমেইল পাঠানো হয়েছে")

    send_verification_email.short_description = "ভেরিফিকেশন ইমেইল পাঠান"

    def send_welcome_email(self, request, queryset):
        sent_count = 0
        for subscriber in queryset.filter(is_verified=True):
            subscriber.send_welcome_email()
            sent_count += 1
        self.message_user(request, f"{sent_count} জনের কাছে স্বাগতম ইমেইল পাঠানো হয়েছে")

    send_welcome_email.short_description = "স্বাগতম ইমেইল পাঠান"

    def save_model(self, request, obj, form, change):
        if not change and not obj.verification_token:
            obj.verification_token = str(uuid.uuid4())

        super().save_model(request, obj, form, change)

        if not change and not obj.is_verified:
            try:
                obj.send_verification_email()
            except Exception:
                self.message_user(
                    request,
                    f"{obj.email} এ ভেরিফিকেশন ইমেইল পাঠানো যায়নি",
                    level="error",
                )