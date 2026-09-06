import os
import uuid
import mimetypes
import urllib.parse
import boto3
from botocore.handlers import validate_bucket_name
from django.utils.text import slugify


def _get_config(key, default=""):
    try:
        from django.conf import settings
        val = getattr(settings, key, None)
        if val:
            return val
    except Exception:
        pass
    return os.getenv(key, default)


def get_s3_client():
    endpoint_url = _get_config("SUPABASE_S3_ENDPOINT_URL")
    access_key_id = _get_config("SUPABASE_S3_ACCESS_KEY_ID")
    secret_access_key = _get_config("SUPABASE_S3_SECRET_ACCESS_KEY")
    region_name = _get_config("SUPABASE_S3_REGION_NAME", "ap-southeast-1")

    client = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        region_name=region_name,
    )

    # Disable botocore's strict S3 bucket name regex check so buckets with spaces or apostrophes (e.g. "Reader's love") work smoothly
    try:
        client.meta.events.unregister("before-parameter-build.s3", validate_bucket_name)
    except Exception:
        pass

    return client


def upload_file_to_supabase(uploaded_file, bucket_name="Articles_Essays", folder="images"):
    """
    Uploads an uploaded file (from request.FILES or FileField) to Supabase Storage via S3 API.
    Returns the public URL of the uploaded file.
    """
    if not uploaded_file:
        return None

    s3 = get_s3_client()

    # Extract clean filename and extension
    original_name = getattr(uploaded_file, "name", "file")
    name_parts = os.path.splitext(original_name)
    raw_name = name_parts[0]
    extension = name_parts[1].lower() if len(name_parts) > 1 else ""

    slug_name = slugify(raw_name)
    if not slug_name:
        slug_name = "file"

    unique_id = uuid.uuid4().hex[:8]
    object_filename = f"{slug_name}-{unique_id}{extension}"

    clean_folder = folder.strip("/")
    object_key = f"{clean_folder}/{object_filename}" if clean_folder else object_filename

    # Determine content type
    content_type = getattr(uploaded_file, "content_type", None)
    if not content_type:
        content_type, _ = mimetypes.guess_type(original_name)
    if not content_type:
        content_type = "application/octet-stream"

    # Reset pointer if it has seek
    if hasattr(uploaded_file, "seek"):
        uploaded_file.seek(0)

    file_bytes = uploaded_file.read()

    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=file_bytes,
        ContentType=content_type,
    )

    supabase_url = _get_config(
        "SUPABASE_URL",
        "https://mmcyfjqjlfernxfluupw.supabase.co",
    ).rstrip("/")

    # URL encode bucket name to safely support spaces and special characters
    quoted_bucket = urllib.parse.quote(bucket_name)
    public_url = f"{supabase_url}/storage/v1/object/public/{quoted_bucket}/{object_key}"
    return public_url
