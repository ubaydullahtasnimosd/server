import os
from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import Culture, History, Misecllaneous, Politics, Travel, Worldview
from server.supabase_storage import upload_file_to_supabase


ALLOWED_VIDEO_EXTENSIONS = [".mp4", ".webm", ".mov", ".mkv", ".avi"]
MAX_VIDEO_SIZE_MB = 50
MAX_VIDEO_SIZE_BYTES = MAX_VIDEO_SIZE_MB * 1024 * 1024  # 50MB in bytes

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


def validate_video_file(file):
    """
    Validates file extension and maximum file size (50MB).
    """
    if not file:
        return

    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_VIDEO_EXTENSIONS:
        allowed_str = ", ".join(e.strip(".").upper() for e in ALLOWED_VIDEO_EXTENSIONS)
        raise ValidationError(
            f"অননুমোদিত ভিডিও ফরম্যাট '{ext}'! শুধুমাত্র {allowed_str} ফরম্যাটের ভিডিও গ্রহণযোগ্য।"
        )

    if file.size > MAX_VIDEO_SIZE_BYTES:
        size_in_mb = round(file.size / (1024 * 1024), 2)
        raise ValidationError(
            f"ভিডিও সাইজ ({size_in_mb} MB) সর্বোচ্চ সীমার চেয়ে বেশি! সর্বোচ্চ {MAX_VIDEO_SIZE_MB} MB সাইজের ভিডিও আপলোড করা যাবে।"
        )


class MisecllaneousAdminForm(forms.ModelForm):
    upload_video = forms.FileField(
        required=False,
        label="নতুন ভিডিও ফাইল আপলোড করুন (Upload Video)",
        help_text="মোবাইল বা কম্পিউটার থেকে ভিডিও সিলেক্ট করুন। অনুমোদিত ফরম্যাট: MP4, WEBM, MOV, MKV, AVI (সর্বোচ্চ ৫০ MB)। এটি Supabase এর Miscellaneous বাকেটে জমা হবে।",
        widget=forms.FileInput(attrs={"accept": ".mp4,.webm,.mov,.mkv,.avi,video/*"})
    )

    class Meta:
        model = Misecllaneous
        fields = "__all__"

    def clean_upload_video(self):
        file = self.cleaned_data.get("upload_video")
        if file:
            validate_video_file(file)
        return file

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "misecllaneousVideo" in self.fields:
            self.fields["misecllaneousVideo"].required = False
            self.fields["misecllaneousVideo"].label = "ভিডিও লিংক / URL (স্বয়ংক্রিয়ভাবে তৈরি হবে অথবা ইউটিউব/অন্যান্য লিংক)"


@admin.register(Misecllaneous)
class MisecllaneousAdmin(ModelAdmin):
    form = MisecllaneousAdminForm

    list_display = (
        "id",
        "misecllaneousTitle",
        "video_preview_link",
        "misecllaneousCreateAt",
    )

    search_fields = (
        "misecllaneousTitle",
        "misecllaneousVideo",
    )

    list_filter = (
        "misecllaneousCreateAt",
    )

    ordering = ("-misecllaneousCreateAt",)

    list_per_page = 20

    readonly_fields = (
        "current_video_preview",
        "misecllaneousCreateAt",
    )

    fieldsets = (
        ("ভিডিও তথ্য (Video Information)", {
            "fields": (
                "upload_video",
                "current_video_preview",
                "misecllaneousTitle",
                "misecllaneousVideo",
            )
        }),
        ("তারিখ ও সময় (Timestamp)", {
            "fields": (
                "misecllaneousCreateAt",
            )
        }),
    )

    def current_video_preview(self, obj):
        video_url = getattr(obj, "misecllaneousVideo", "")
        if not video_url:
            return "কোনো ভিডিও যুক্ত করা নেই"

        lower_url = video_url.lower()
        if any(lower_url.endswith(ext) for ext in [".mp4", ".webm", ".mov", ".mkv", ".avi", ".ogg"]) or "supabase.co" in lower_url:
            return format_html(
                '<div style="margin-top: 4px;">'
                '<video src="{}" controls style="max-height: 220px; max-width: 400px; border-radius: 8px; background: #000;" preload="metadata"></video>'
                '<div style="font-size: 11px; color: #64748b; margin-top: 4px; word-break: break-all;">{}</div>'
                '</div>',
                video_url, video_url
            )
        else:
            return format_html(
                '<div style="margin-top: 4px;">'
                '<iframe src="{}" width="400" height="220" style="border-radius: 8px; border: 1px solid #e2e8f0;" allowfullscreen></iframe>'
                '<div style="font-size: 11px; color: #64748b; margin-top: 4px; word-break: break-all;">{}</div>'
                '</div>',
                video_url, video_url
            )
    current_video_preview.short_description = "বর্তমান ভিডিও প্রিভিউ (Current Video Preview)"

    def video_preview_link(self, obj):
        url = obj.misecllaneousVideo
        if not url:
            return "-"
        return format_html(
            '<a href="{}" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; gap: 4px; padding: 4px 10px; background: #eff6ff; color: #2563eb; border-radius: 6px; font-weight: 500; font-size: 12px; text-decoration: none;">'
            '▶ প্লে / লিঙ্ক'
            '</a>',
            url
        )
    video_preview_link.short_description = "ভিডিও প্লে"

    def save_model(self, request, obj, form, change):
        video_file = form.cleaned_data.get("upload_video")
        if video_file:
            uploaded_url = upload_file_to_supabase(
                video_file,
                bucket_name="Miscellaneous",
                folder="videos"
            )
            if uploaded_url:
                obj.misecllaneousVideo = uploaded_url

        super().save_model(request, obj, form, change)


class CultureAdminForm(forms.ModelForm):
    upload_content_image = forms.ImageField(
        required=False,
        label="নতুন ছবি আপলোড করুন (Upload Image)",
        help_text="মোবাইল বা কম্পিউটার থেকে ছবি সিলেক্ট করুন। অনুমোদিত ফরম্যাট: JPG, PNG, JPEG, WEBP (সর্বোচ্চ ২ MB)। এটি Supabase এর Culture বাকেটে জমা হবে।",
        widget=forms.FileInput(attrs={"accept": ".jpg,.jpeg,.png,.webp"})
    )

    class Meta:
        model = Culture
        fields = "__all__"

    def clean_upload_content_image(self):
        file = self.cleaned_data.get("upload_content_image")
        if file:
            validate_image_file(file)
        return file

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "contentImg" in self.fields:
            self.fields["contentImg"].required = False
            self.fields["contentImg"].label = "ছবির লিংক / URL (স্বয়ংক্রিয়ভাবে তৈরি হবে অথবা ম্যানুয়াল লিংক)"


@admin.register(Culture)
class CultureAdmin(ModelAdmin):
    form = CultureAdminForm

    list_display = (
        "id",
        "content_image_preview",
        "contentName",
        "contentAuthor",
        "contentCreateAt",
    )
    search_fields = (
        "contentName",
        "contentAuthor",
        "contentDescription",
    )
    list_filter = ("contentCreateAt",)
    ordering = ("-contentCreateAt",)
    list_per_page = 20
    readonly_fields = (
        "current_content_image",
        "contentCreateAt",
        "contentUpdateAt",
    )
    fieldsets = (
        (
            "কালচার ও সংস্কৃতি তথ্য (Culture Information)",
            {
                "fields": (
                    "upload_content_image",
                    "current_content_image",
                    "contentImg",
                    "contentName",
                    "contentAuthor",
                    "contentDescription",
                )
            },
        ),
        (
            "তারিখ ও সময় (Timestamps)",
            {"fields": ("contentCreateAt", "contentUpdateAt")},
        ),
    )

    def current_content_image(self, obj):
        image_url = get_image_url(obj.contentImg) if obj else None
        if not image_url:
            return "কোনো ছবি যুক্ত করা নেই"
        return format_html(
            '<div style="margin-top: 4px;">'
            '<a href="{}" target="_blank" rel="noopener noreferrer">'
            '<img src="{}" style="max-height: 180px; max-width: 260px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); object-fit: cover;" />'
            '</a>'
            '<div style="font-size: 11px; color: #64748b; margin-top: 4px; word-break: break-all;">{}</div>'
            '</div>',
            image_url, image_url, image_url
        )
    current_content_image.short_description = "বর্তমান ছবি প্রিভিউ (Current Image Preview)"

    @admin.display(description="ছবি")
    def content_image_preview(self, obj):
        image_url = get_image_url(obj.contentImg)
        if not image_url:
            return "-"

        return format_html(
            '<img src="{}" width="60" height="60" style="border-radius:6px; object-fit:cover; box-shadow: 0 1px 3px rgba(0,0,0,0.1);" />',
            image_url,
        )

    def save_model(self, request, obj, form, change):
        image_file = form.cleaned_data.get("upload_content_image")
        if image_file:
            uploaded_url = upload_file_to_supabase(
                image_file,
                bucket_name="Culture",
                folder="culture"
            )
            if uploaded_url:
                obj.contentImg = uploaded_url

        super().save_model(request, obj, form, change)


class MiscellaneousContentAdmin(ModelAdmin):
    list_display = (
        "id",
        "content_image_preview",
        "contentName",
        "contentAuthor",
        "contentCreateAt",
    )
    search_fields = (
        "contentName",
        "contentAuthor",
        "contentDescription",
    )
    list_filter = ("contentCreateAt",)
    ordering = ("-contentCreateAt",)
    list_per_page = 20
    readonly_fields = ("contentCreateAt", "contentUpdateAt")
    fieldsets = (
        (
            "Content Information",
            {
                "fields": (
                    "contentImg",
                    "contentName",
                    "contentAuthor",
                    "contentDescription",
                )
            },
        ),
        (
            "Timestamps",
            {"fields": ("contentCreateAt", "contentUpdateAt")},
        ),
    )

    @admin.display(description="Content Image")
    def content_image_preview(self, obj):
        if not obj.contentImg:
            return "-"

        return format_html(
            '<img src="{}" width="60" height="60" style="border-radius:6px; object-fit:cover;" />',
            obj.contentImg,
        )


class TravelAdminForm(forms.ModelForm):
    upload_content_image = forms.ImageField(
        required=False,
        label="নতুন ছবি আপলোড করুন (Upload Image)",
        help_text="মোবাইল বা কম্পিউটার থেকে ছবি সিলেক্ট করুন। অনুমোদিত ফরম্যাট: JPG, PNG, JPEG, WEBP (সর্বোচ্চ ২ MB)। এটি Supabase এর Travel বাকেটে জমা হবে।",
        widget=forms.FileInput(attrs={"accept": ".jpg,.jpeg,.png,.webp"})
    )

    class Meta:
        model = Travel
        fields = "__all__"

    def clean_upload_content_image(self):
        file = self.cleaned_data.get("upload_content_image")
        if file:
            validate_image_file(file)
        return file

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "contentImg" in self.fields:
            self.fields["contentImg"].required = False
            self.fields["contentImg"].label = "ছবির লিংক / URL (স্বয়ংক্রিয়ভাবে তৈরি হবে অথবা ম্যানুয়াল লিংক)"


@admin.register(Travel)
class TravelAdmin(ModelAdmin):
    form = TravelAdminForm

    list_display = (
        "id",
        "content_image_preview",
        "contentName",
        "contentAuthor",
        "contentCreateAt",
    )
    search_fields = (
        "contentName",
        "contentAuthor",
        "contentDescription",
    )
    list_filter = ("contentCreateAt",)
    ordering = ("-contentCreateAt",)
    list_per_page = 20
    readonly_fields = (
        "current_content_image",
        "contentCreateAt",
        "contentUpdateAt",
    )
    fieldsets = (
        (
            "ভ্রমণ সংক্রান্ত তথ্য (Travel Information)",
            {
                "fields": (
                    "upload_content_image",
                    "current_content_image",
                    "contentImg",
                    "contentName",
                    "contentAuthor",
                    "contentDescription",
                )
            },
        ),
        (
            "তারিখ ও সময় (Timestamps)",
            {"fields": ("contentCreateAt", "contentUpdateAt")},
        ),
    )

    def current_content_image(self, obj):
        image_url = get_image_url(obj.contentImg) if obj else None
        if not image_url:
            return "কোনো ছবি যুক্ত করা নেই"
        return format_html(
            '<div style="margin-top: 4px;">'
            '<a href="{}" target="_blank" rel="noopener noreferrer">'
            '<img src="{}" style="max-height: 180px; max-width: 260px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); object-fit: cover;" />'
            '</a>'
            '<div style="font-size: 11px; color: #64748b; margin-top: 4px; word-break: break-all;">{}</div>'
            '</div>',
            image_url, image_url, image_url
        )
    current_content_image.short_description = "বর্তমান ছবি প্রিভিউ (Current Image Preview)"

    @admin.display(description="ছবি")
    def content_image_preview(self, obj):
        image_url = get_image_url(obj.contentImg)
        if not image_url:
            return "-"

        return format_html(
            '<img src="{}" width="60" height="60" style="border-radius:6px; object-fit:cover; box-shadow: 0 1px 3px rgba(0,0,0,0.1);" />',
            image_url,
        )

    def save_model(self, request, obj, form, change):
        image_file = form.cleaned_data.get("upload_content_image")
        if image_file:
            uploaded_url = upload_file_to_supabase(
                image_file,
                bucket_name="Travel",
                folder="travel"
            )
            if uploaded_url:
                obj.contentImg = uploaded_url

        super().save_model(request, obj, form, change)


class HistoryAdminForm(forms.ModelForm):
    upload_content_image = forms.ImageField(
        required=False,
        label="নতুন ছবি আপলোড করুন (Upload Image)",
        help_text="মোবাইল বা কম্পিউটার থেকে ছবি সিলেক্ট করুন। অনুমোদিত ফরম্যাট: JPG, PNG, JPEG, WEBP (সর্বোচ্চ ২ MB)। এটি Supabase এর History বাকেটে জমা হবে।",
        widget=forms.FileInput(attrs={"accept": ".jpg,.jpeg,.png,.webp"})
    )

    class Meta:
        model = History
        fields = "__all__"

    def clean_upload_content_image(self):
        file = self.cleaned_data.get("upload_content_image")
        if file:
            validate_image_file(file)
        return file

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "contentImg" in self.fields:
            self.fields["contentImg"].required = False
            self.fields["contentImg"].label = "ছবির লিংক / URL (স্বয়ংক্রিয়ভাবে তৈরি হবে অথবা ম্যানুয়াল লিংক)"


@admin.register(History)
class HistoryAdmin(ModelAdmin):
    form = HistoryAdminForm

    list_display = (
        "id",
        "content_image_preview",
        "contentName",
        "contentAuthor",
        "contentCreateAt",
    )
    search_fields = (
        "contentName",
        "contentAuthor",
        "contentDescription",
    )
    list_filter = ("contentCreateAt",)
    ordering = ("-contentCreateAt",)
    list_per_page = 20
    readonly_fields = (
        "current_content_image",
        "contentCreateAt",
        "contentUpdateAt",
    )
    fieldsets = (
        (
            "ইতিহাস সংক্রান্ত তথ্য (History Information)",
            {
                "fields": (
                    "upload_content_image",
                    "current_content_image",
                    "contentImg",
                    "contentName",
                    "contentAuthor",
                    "contentDescription",
                )
            },
        ),
        (
            "তারিখ ও সময় (Timestamps)",
            {"fields": ("contentCreateAt", "contentUpdateAt")},
        ),
    )

    def current_content_image(self, obj):
        image_url = get_image_url(obj.contentImg) if obj else None
        if not image_url:
            return "কোনো ছবি যুক্ত করা নেই"
        return format_html(
            '<div style="margin-top: 4px;">'
            '<a href="{}" target="_blank" rel="noopener noreferrer">'
            '<img src="{}" style="max-height: 180px; max-width: 260px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); object-fit: cover;" />'
            '</a>'
            '<div style="font-size: 11px; color: #64748b; margin-top: 4px; word-break: break-all;">{}</div>'
            '</div>',
            image_url, image_url, image_url
        )
    current_content_image.short_description = "বর্তমান ছবি প্রিভিউ (Current Image Preview)"

    @admin.display(description="ছবি")
    def content_image_preview(self, obj):
        image_url = get_image_url(obj.contentImg)
        if not image_url:
            return "-"

        return format_html(
            '<img src="{}" width="60" height="60" style="border-radius:6px; object-fit:cover; box-shadow: 0 1px 3px rgba(0,0,0,0.1);" />',
            image_url,
        )

    def save_model(self, request, obj, form, change):
        image_file = form.cleaned_data.get("upload_content_image")
        if image_file:
            uploaded_url = upload_file_to_supabase(
                image_file,
                bucket_name="History",
                folder="history"
            )
            if uploaded_url:
                obj.contentImg = uploaded_url

        super().save_model(request, obj, form, change)


class PoliticsAdminForm(forms.ModelForm):
    upload_content_image = forms.ImageField(
        required=False,
        label="নতুন ছবি আপলোড করুন (Upload Image)",
        help_text="মোবাইল বা কম্পিউটার থেকে ছবি সিলেক্ট করুন। অনুমোদিত ফরম্যাট: JPG, PNG, JPEG, WEBP (সর্বোচ্চ ২ MB)। এটি Supabase এর Politics বাকেটে জমা হবে।",
        widget=forms.FileInput(attrs={"accept": ".jpg,.jpeg,.png,.webp"})
    )

    class Meta:
        model = Politics
        fields = "__all__"

    def clean_upload_content_image(self):
        file = self.cleaned_data.get("upload_content_image")
        if file:
            validate_image_file(file)
        return file

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "contentImg" in self.fields:
            self.fields["contentImg"].required = False
            self.fields["contentImg"].label = "ছবির লিংক / URL (স্বয়ংক্রিয়ভাবে তৈরি হবে অথবা ম্যানুয়াল লিংক)"


@admin.register(Politics)
class PoliticsAdmin(ModelAdmin):
    form = PoliticsAdminForm

    list_display = (
        "id",
        "content_image_preview",
        "contentName",
        "contentAuthor",
        "contentCreateAt",
    )
    search_fields = (
        "contentName",
        "contentAuthor",
        "contentDescription",
    )
    list_filter = ("contentCreateAt",)
    ordering = ("-contentCreateAt",)
    list_per_page = 20
    readonly_fields = (
        "current_content_image",
        "contentCreateAt",
        "contentUpdateAt",
    )
    fieldsets = (
        (
            "রাজনীতি সংক্রান্ত তথ্য (Politics Information)",
            {
                "fields": (
                    "upload_content_image",
                    "current_content_image",
                    "contentImg",
                    "contentName",
                    "contentAuthor",
                    "contentDescription",
                )
            },
        ),
        (
            "তারিখ ও সময় (Timestamps)",
            {"fields": ("contentCreateAt", "contentUpdateAt")},
        ),
    )

    def current_content_image(self, obj):
        image_url = get_image_url(obj.contentImg) if obj else None
        if not image_url:
            return "কোনো ছবি যুক্ত করা নেই"
        return format_html(
            '<div style="margin-top: 4px;">'
            '<a href="{}" target="_blank" rel="noopener noreferrer">'
            '<img src="{}" style="max-height: 180px; max-width: 260px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); object-fit: cover;" />'
            '</a>'
            '<div style="font-size: 11px; color: #64748b; margin-top: 4px; word-break: break-all;">{}</div>'
            '</div>',
            image_url, image_url, image_url
        )
    current_content_image.short_description = "বর্তমান ছবি প্রিভিউ (Current Image Preview)"

    @admin.display(description="ছবি")
    def content_image_preview(self, obj):
        image_url = get_image_url(obj.contentImg)
        if not image_url:
            return "-"

        return format_html(
            '<img src="{}" width="60" height="60" style="border-radius:6px; object-fit:cover; box-shadow: 0 1px 3px rgba(0,0,0,0.1);" />',
            image_url,
        )

    def save_model(self, request, obj, form, change):
        image_file = form.cleaned_data.get("upload_content_image")
        if image_file:
            uploaded_url = upload_file_to_supabase(
                image_file,
                bucket_name="Politics",
                folder="politics"
            )
            if uploaded_url:
                obj.contentImg = uploaded_url

        super().save_model(request, obj, form, change)


class WorldviewAdminForm(forms.ModelForm):
    upload_content_image = forms.ImageField(
        required=False,
        label="নতুন ছবি আপলোড করুন (Upload Image)",
        help_text="মোবাইল বা কম্পিউটার থেকে ছবি সিলেক্ট করুন। অনুমোদিত ফরম্যাট: JPG, PNG, JPEG, WEBP (সর্বোচ্চ ২ MB)। এটি Supabase এর Worldview বাকেটে জমা হবে।",
        widget=forms.FileInput(attrs={"accept": ".jpg,.jpeg,.png,.webp"})
    )

    class Meta:
        model = Worldview
        fields = "__all__"

    def clean_upload_content_image(self):
        file = self.cleaned_data.get("upload_content_image")
        if file:
            validate_image_file(file)
        return file

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "contentImg" in self.fields:
            self.fields["contentImg"].required = False
            self.fields["contentImg"].label = "ছবির লিংক / URL (স্বয়ংক্রিয়ভাবে তৈরি হবে অথবা ম্যানুয়াল লিংক)"


@admin.register(Worldview)
class WorldviewAdmin(ModelAdmin):
    form = WorldviewAdminForm

    list_display = (
        "id",
        "content_image_preview",
        "contentName",
        "contentAuthor",
        "contentCreateAt",
    )
    search_fields = (
        "contentName",
        "contentAuthor",
        "contentDescription",
    )
    list_filter = ("contentCreateAt",)
    ordering = ("-contentCreateAt",)
    list_per_page = 20
    readonly_fields = (
        "current_content_image",
        "contentCreateAt",
        "contentUpdateAt",
    )
    fieldsets = (
        (
            "বিশ্ব-দর্শন সংক্রান্ত তথ্য (Worldview Information)",
            {
                "fields": (
                    "upload_content_image",
                    "current_content_image",
                    "contentImg",
                    "contentName",
                    "contentAuthor",
                    "contentDescription",
                )
            },
        ),
        (
            "তারিখ ও সময় (Timestamps)",
            {"fields": ("contentCreateAt", "contentUpdateAt")},
        ),
    )

    def current_content_image(self, obj):
        image_url = get_image_url(obj.contentImg) if obj else None
        if not image_url:
            return "কোনো ছবি যুক্ত করা নেই"
        return format_html(
            '<div style="margin-top: 4px;">'
            '<a href="{}" target="_blank" rel="noopener noreferrer">'
            '<img src="{}" style="max-height: 180px; max-width: 260px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); object-fit: cover;" />'
            '</a>'
            '<div style="font-size: 11px; color: #64748b; margin-top: 4px; word-break: break-all;">{}</div>'
            '</div>',
            image_url, image_url, image_url
        )
    current_content_image.short_description = "বর্তমান ছবি প্রিভিউ (Current Image Preview)"

    @admin.display(description="ছবি")
    def content_image_preview(self, obj):
        image_url = get_image_url(obj.contentImg)
        if not image_url:
            return "-"

        return format_html(
            '<img src="{}" width="60" height="60" style="border-radius:6px; object-fit:cover; box-shadow: 0 1px 3px rgba(0,0,0,0.1);" />',
            image_url,
        )

    def save_model(self, request, obj, form, change):
        image_file = form.cleaned_data.get("upload_content_image")
        if image_file:
            uploaded_url = upload_file_to_supabase(
                image_file,
                bucket_name="Worldview",
                folder="worldview"
            )
            if uploaded_url:
                obj.contentImg = uploaded_url

        super().save_model(request, obj, form, change)
