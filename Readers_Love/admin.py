import os
from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import Readers_Love, Readers_Love_Img
from server.supabase_storage import upload_file_to_supabase


ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"]
MAX_IMAGE_SIZE_MB = 2
MAX_IMAGE_SIZE_BYTES = MAX_IMAGE_SIZE_MB * 1024 * 1024  # 2MB in bytes


def get_image_url(image_field):
    if not image_field:
        return None
    try:
        return image_field.url
    except AttributeError:
        return str(image_field).strip()


def validate_image_file(file):
    """
    Validates file extension and maximum file size (2MB).
    """
    if not file:
        return

    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        allowed_str = ", ".join(e.strip(".").upper() for e in ALLOWED_IMAGE_EXTENSIONS)
        raise ValidationError(
            f"অননুমোদিত ফাইল ফরম্যাট '{ext}'! শুধুমাত্র {allowed_str} ফরম্যাট গ্রহণযোগ্য।"
        )

    if file.size > MAX_IMAGE_SIZE_BYTES:
        size_in_mb = round(file.size / (1024 * 1024), 2)
        raise ValidationError(
            f"ফাইলের সাইজ ({size_in_mb} MB) অনেক বড়! সর্বোচ্চ {MAX_IMAGE_SIZE_MB} MB সাইজের ছবি আপলোড করা যাবে।"
        )


class ReadersLoveImgAdminForm(forms.ModelForm):
    upload_book_image = forms.ImageField(
        required=False,
        label="নতুন রিভিউ ছবি আপলোড করুন (Upload Reader Image)",
        help_text="মোবাইল বা কম্পিউটার থেকে পাঠকের রিভিউ ছবি সিলেক্ট করুন। অনুমোদিত ফরম্যাট: JPG, PNG, JPEG, WEBP (সর্বোচ্চ ২ MB)। এটি Supabase এর Reader's love বাকেটে জমা হবে।",
        widget=forms.FileInput(attrs={"accept": ".jpg,.jpeg,.png,.webp"})
    )

    class Meta:
        model = Readers_Love_Img
        fields = "__all__"

    def clean_upload_book_image(self):
        file = self.cleaned_data.get("upload_book_image")
        if file:
            validate_image_file(file)
        return file

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "readersBookImg" in self.fields:
            self.fields["readersBookImg"].required = False
            self.fields["readersBookImg"].label = "ছবির লিংক / URL (স্বয়ংক্রিয়ভাবে তৈরি হবে অথবা ম্যানুয়াল লিংক)"


@admin.register(Readers_Love)
class ReadersLoveAdmin(ModelAdmin):
    list_display = (
        "id",
        "readersBookName",
        "readersName",
        "short_review",
        "readersReviewCreated",
    )

    search_fields = (
        "readersBookName",
        "readersName",
        "readersReview",
    )

    list_filter = (
        "readersReviewCreated",
    )

    ordering = ("-readersReviewCreated",)

    list_per_page = 20

    readonly_fields = (
        "readersReviewCreated",
    )

    fieldsets = (
        ("পাঠক রিভিউ তথ্য (Reader Review Information)", {
            "fields": (
                "readersBookName",
                "readersName",
                "readersReview",
            )
        }),
        ("তারিখ ও সময় (Timestamp)", {
            "fields": (
                "readersReviewCreated",
            )
        }),
    )

    def short_review(self, obj):
        if obj.readersReview:
            return obj.readersReview[:80] + "..." if len(obj.readersReview) > 80 else obj.readersReview
        return "-"

    short_review.short_description = "রিভিউ"


@admin.register(Readers_Love_Img)
class ReadersLoveImgAdmin(ModelAdmin):
    form = ReadersLoveImgAdminForm

    list_display = (
        "id",
        "image_preview",
        "readersReviewCreated",
    )

    list_filter = (
        "readersReviewCreated",
    )

    ordering = ("-readersReviewCreated",)

    list_per_page = 20

    readonly_fields = (
        "current_image_preview",
        "readersReviewCreated",
    )

    fieldsets = (
        ("ছবির তথ্য (Image Information)", {
            "fields": (
                "upload_book_image",
                "current_image_preview",
                "readersBookImg",
            )
        }),
        ("তারিখ ও সময় (Timestamp)", {
            "fields": (
                "readersReviewCreated",
            )
        }),
    )

    def current_image_preview(self, obj):
        image_url = get_image_url(obj.readersBookImg) if obj else None
        if not image_url:
            return "কোনো ছবি যুক্ত করা নেই"
        return format_html(
            '<div style="margin-top: 4px;">'
            '<a href="{}" target="_blank" rel="noopener noreferrer">'
            '<img src="{}" style="max-height: 180px; max-width: 240px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); object-fit: cover;" />'
            '</a>'
            '<div style="font-size: 11px; color: #64748b; margin-top: 4px; word-break: break-all;">{}</div>'
            '</div>',
            image_url, image_url, image_url
        )
    current_image_preview.short_description = "বর্তমান ছবি প্রিভিউ (Current Image Preview)"

    def image_preview(self, obj):
        image_url = get_image_url(obj.readersBookImg)
        if not image_url:
            return "-"
        return format_html(
            '<img src="{}" width="60" height="60" style="border-radius:6px; object-fit:cover; box-shadow: 0 1px 3px rgba(0,0,0,0.1);" />',
            image_url
        )

    image_preview.short_description = "ছবি"

    def save_model(self, request, obj, form, change):
        image_file = form.cleaned_data.get("upload_book_image")
        if image_file:
            uploaded_url = upload_file_to_supabase(
                image_file,
                bucket_name="Reader's love",
                folder="readers"
            )
            if uploaded_url:
                obj.readersBookImg = uploaded_url

        super().save_model(request, obj, form, change)