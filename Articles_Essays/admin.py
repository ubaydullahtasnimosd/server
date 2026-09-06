import os
from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import Articles_Essays
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

    # Check file extension
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        allowed_str = ", ".join(ext.strip(".").upper() for ext in ALLOWED_IMAGE_EXTENSIONS)
        raise ValidationError(
            f"অননুমোদিত ফাইল ফরম্যাট '{ext}'! শুধুমাত্র {allowed_str} ফরম্যাট গ্রহণযোগ্য।"
        )

    # Check file size (max 2MB)
    if file.size > MAX_IMAGE_SIZE_BYTES:
        size_in_mb = round(file.size / (1024 * 1024), 2)
        raise ValidationError(
            f"ফাইলের সাইজ ({size_in_mb} MB) সর্বোচ্চ সীমার চেয়ে বেশি! দয়া করে সর্বোচ্চ {MAX_IMAGE_SIZE_MB} MB সাইজের ছবি নির্বাচন করুন।"
        )


class ArticlesEssaysAdminForm(forms.ModelForm):
    upload_article_image = forms.ImageField(
        required=False,
        label="নতুন ইমেজ আপলোড করুন (Upload Image)",
        help_text="অনুমোদিত ফরম্যাট: JPG, PNG, JPEG, WEBP (সর্বোচ্চ সাইজ: ২ MB)। এটি Supabase এর Articles ফোল্ডারে জমা হবে।",
        widget=forms.FileInput(attrs={"accept": ".jpg,.jpeg,.png,.webp"})
    )
    upload_qr_image = forms.ImageField(
        required=False,
        label="নতুন QR কোড স্ক্যান ছবি আপলোড করুন (Upload QR Image)",
        help_text="অনুমোদিত ফরম্যাট: JPG, PNG, JPEG, WEBP (সর্বোচ্চ সাইজ: ২ MB)। এটি Supabase এর qrcode-scen ফোল্ডারে জমা হবে।",
        widget=forms.FileInput(attrs={"accept": ".jpg,.jpeg,.png,.webp"})
    )

    class Meta:
        model = Articles_Essays
        fields = "__all__"

    def clean_upload_article_image(self):
        file = self.cleaned_data.get("upload_article_image")
        if file:
            validate_image_file(file)
        return file

    def clean_upload_qr_image(self):
        file = self.cleaned_data.get("upload_qr_image")
        if file:
            validate_image_file(file)
        return file

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make direct URL fields optional and styled as fallback
        if "articlesEssaysImg" in self.fields:
            self.fields["articlesEssaysImg"].required = False
            self.fields["articlesEssaysImg"].label = "ইমেজ URL (স্বয়ংক্রিয়ভাবে তৈরি হবে অথবা ম্যানুয়াল লিংক)"
        if "articlesEssaysQRCodeScenImg" in self.fields:
            self.fields["articlesEssaysQRCodeScenImg"].required = False
            self.fields["articlesEssaysQRCodeScenImg"].label = "QR ইমেজ URL (স্বয়ংক্রিয়ভাবে তৈরি হবে অথবা ম্যানুয়াল লিংক)"


@admin.register(Articles_Essays)
class ArticlesEssaysAdmin(ModelAdmin):
    form = ArticlesEssaysAdminForm

    list_display = (
        "id",
        "article_image_preview",
        "articlesEssaysName",
        "articlesEssaysAuthor",
        "qr_image_preview",
        "articlesEssaysQRCodeScen",
        "articlesEssaysCreateAt",
    )

    search_fields = (
        "articlesEssaysName",
        "articlesEssaysAuthor",
        "articlesEssaysDescription",
        "articlesEssaysQRCodeScen",
    )

    list_filter = (
        "articlesEssaysCreateAt",
    )

    ordering = ("-articlesEssaysCreateAt",)

    list_per_page = 20

    readonly_fields = (
        "current_article_image",
        "current_qr_image",
        "articlesEssaysCreateAt",
        "articlesEssaysUpdateAt",
    )

    fieldsets = (
        ("প্রবন্ধ-নিবন্ধ তথ্য (Article Information)", {
            "fields": (
                "upload_article_image",
                "current_article_image",
                "articlesEssaysImg",
                "articlesEssaysName",
                "articlesEssaysAuthor",
                "articlesEssaysDescription",
            )
        }),
        ("QR কোড তথ্য (QR Code Information)", {
            "fields": (
                "upload_qr_image",
                "current_qr_image",
                "articlesEssaysQRCodeScen",
                "articlesEssaysQRCodeScenImg",
            )
        }),
        ("তারিখ ও সময় (Timestamps)", {
            "fields": (
                "articlesEssaysCreateAt",
                "articlesEssaysUpdateAt",
            )
        }),
    )

    def current_article_image(self, obj):
        image_url = get_image_url(obj.articlesEssaysImg) if obj else None
        if not image_url:
            return "কোনো ইমেজ যুক্ত করা নেই"
        return format_html(
            '<div style="margin-top: 4px;">'
            '<a href="{}" target="_blank" rel="noopener noreferrer">'
            '<img src="{}" style="max-height: 140px; max-width: 240px; border-radius: 8px; border: 1px solid #e2e8f0; object-fit: cover;" />'
            '</a>'
            '<div style="font-size: 11px; color: #64748b; margin-top: 4px; word-break: break-all;">{}</div>'
            '</div>',
            image_url, image_url, image_url
        )
    current_article_image.short_description = "বর্তমান ইমেজ (Current Image Preview)"

    def current_qr_image(self, obj):
        image_url = get_image_url(obj.articlesEssaysQRCodeScenImg) if obj else None
        if not image_url:
            return "কোনো QR ইমেজ যুক্ত করা নেই"
        return format_html(
            '<div style="margin-top: 4px;">'
            '<a href="{}" target="_blank" rel="noopener noreferrer">'
            '<img src="{}" style="max-height: 140px; max-width: 240px; border-radius: 8px; border: 1px solid #e2e8f0; object-fit: cover;" />'
            '</a>'
            '<div style="font-size: 11px; color: #64748b; margin-top: 4px; word-break: break-all;">{}</div>'
            '</div>',
            image_url, image_url, image_url
        )
    current_qr_image.short_description = "বর্তমান QR কোড ইমেজ (Current QR Image Preview)"

    def article_image_preview(self, obj):
        image_url = get_image_url(obj.articlesEssaysImg)
        if not image_url:
            return "-"
        return format_html(
            '<img src="{}" width="50" height="50" style="border-radius:6px; object-fit:cover;" />',
            image_url
        )
    article_image_preview.short_description = "ইমেজ"

    def qr_image_preview(self, obj):
        image_url = get_image_url(obj.articlesEssaysQRCodeScenImg)
        if not image_url:
            return "-"
        return format_html(
            '<img src="{}" width="50" height="50" style="border-radius:6px; object-fit:cover;" />',
            image_url
        )
    qr_image_preview.short_description = "QR ইমেজ"

    def save_model(self, request, obj, form, change):
        # 1. Articles_Essays এর ছবি -> "Articles" ফোল্ডারে আপলোড
        article_file = form.cleaned_data.get("upload_article_image")
        if article_file:
            uploaded_url = upload_file_to_supabase(
                article_file,
                bucket_name="Articles_Essays",
                folder="Articles"
            )
            if uploaded_url:
                obj.articlesEssaysImg = uploaded_url

        # 2. qrcode-scen এর ছবি -> "qrcode-scen" ফোল্ডারে আপলোড
        qr_file = form.cleaned_data.get("upload_qr_image")
        if qr_file:
            uploaded_qr_url = upload_file_to_supabase(
                qr_file,
                bucket_name="Articles_Essays",
                folder="qrcode-scen"
            )
            if uploaded_qr_url:
                obj.articlesEssaysQRCodeScenImg = uploaded_qr_url

        super().save_model(request, obj, form, change)