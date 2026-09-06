import os
from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import Book
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


class BookAdminForm(forms.ModelForm):
    upload_book_image = forms.ImageField(
        required=False,
        label="নতুন বইয়ের কভার ইমেজ আপলোড করুন (Upload Book Cover)",
        help_text="মোবাইল বা কম্পিউটার থেকে কভার ছবি সিলেক্ট করুন। অনুমোদিত ফরম্যাট: JPG, PNG, JPEG, WEBP (সর্বোচ্চ ২ MB)। এটি Supabase এর Books বাকেটে জমা হবে।",
        widget=forms.FileInput(attrs={"accept": ".jpg,.jpeg,.png,.webp"})
    )

    class Meta:
        model = Book
        fields = "__all__"

    def clean_upload_book_image(self):
        file = self.cleaned_data.get("upload_book_image")
        if file:
            validate_image_file(file)
        return file

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "bookImage" in self.fields:
            self.fields["bookImage"].required = False
            self.fields["bookImage"].label = "বইয়ের ছবির লিংক / URL (স্বয়ংক্রিয়ভাবে তৈরি হবে অথবা ম্যানুয়াল লিংক)"


@admin.register(Book)
class BookAdmin(ModelAdmin):
    form = BookAdminForm

    list_display = (
        "id",
        "book_image_preview",
        "bookTitle",
        "bookPublication",
        "short_description",
        "bookPurchaseLink",
        "bookCreatedAt",
    )

    search_fields = (
        "bookTitle",
        "bookPublication",
        "bookDescription",
        "bookPurchaseLink",
    )

    list_filter = (
        "bookCreatedAt",
    )

    ordering = ("-bookCreatedAt",)

    list_per_page = 20

    readonly_fields = (
        "current_book_image",
        "bookCreatedAt",
        "bookUpdateAt",
    )

    fieldsets = (
        ("বইয়ের তথ্য (Book Information)", {
            "fields": (
                "upload_book_image",
                "current_book_image",
                "bookImage",
                "bookTitle",
                "bookPublication",
                "bookDescription",
                "bookPurchaseLink",
            )
        }),
        ("তারিখ ও সময় (Timestamps)", {
            "fields": (
                "bookCreatedAt",
                "bookUpdateAt",
            )
        }),
    )

    def current_book_image(self, obj):
        image_url = get_image_url(obj.bookImage) if obj else None
        if not image_url:
            return "কোনো কভার ছবি যুক্ত করা নেই"
        return format_html(
            '<div style="margin-top: 4px;">'
            '<a href="{}" target="_blank" rel="noopener noreferrer">'
            '<img src="{}" style="max-height: 180px; max-width: 240px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); object-fit: cover;" />'
            '</a>'
            '<div style="font-size: 11px; color: #64748b; margin-top: 4px; word-break: break-all;">{}</div>'
            '</div>',
            image_url, image_url, image_url
        )
    current_book_image.short_description = "বর্তমান বইয়ের কভার (Current Cover Preview)"

    def book_image_preview(self, obj):
        image_url = get_image_url(obj.bookImage)
        if not image_url:
            return "-"
        return format_html(
            '<img src="{}" width="50" height="65" style="border-radius:6px; object-fit:cover; box-shadow: 0 1px 3px rgba(0,0,0,0.1);" />',
            image_url
        )
    book_image_preview.short_description = "কভার"

    def short_description(self, obj):
        if obj.bookDescription:
            return obj.bookDescription[:80] + "..." if len(obj.bookDescription) > 80 else obj.bookDescription
        return "-"
    short_description.short_description = "বিবরণ"

    def save_model(self, request, obj, form, change):
        cover_file = form.cleaned_data.get("upload_book_image")
        if cover_file:
            uploaded_url = upload_file_to_supabase(
                cover_file,
                bucket_name="Books",
                folder="covers"
            )
            if uploaded_url:
                obj.bookImage = uploaded_url

        super().save_model(request, obj, form, change)