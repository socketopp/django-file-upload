from celery import shared_task
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import ImageUpload
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import base64
from django.utils import timezone
import mimetypes


@shared_task
def process_and_save_image(image_bytes, file_name, file_size, file_type, image_instance_id):
    """
    Process and save an uploaded image asynchronously.

    This task performs the following operations:
    1. Retrieves the ImageUpload instance from the database.
    2. Sends a notification that processing has started.
    3. Opens and processes the image (resizing and format conversion if necessary).
    4. Saves the processed image and updates the ImageUpload instance.
    5. Sends a notification that processing is complete.

    Args:
        image_bytes (bytes): The raw image data.
        file_name (str): The original filename, containing job_id and name separated by ';;'.
        file_size (int): The size of the original file in bytes.
        file_type (str): The MIME type of the image.
        image_instance_id (UUID): The ID of the corresponding ImageUpload instance.

    Raises:
        Exception: If the ImageUpload instance doesn't exist or if image processing fails.

    Note:
        This function is decorated with @shared_task, allowing it to be executed by Celery workers.
    """
    job_id, name = file_name.split(';;')

    try:
        image_instance = ImageUpload.objects.get(id=image_instance_id)
    except ImageUpload.DoesNotExist:
        raise Exception("Image instance does not exist")

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'upload_group',
        {
            'type': 'send_upload_notification',
            'job_id': str(job_id),
            'status': 'processing',
            'message': f'Image {name} processing.'
        }
    )
    
    try:
        img_io = io.BytesIO(image_bytes)
        img = Image.open(img_io)
    except Exception as e:
        image_instance.status = 'error'
        image_instance.save()
        raise Exception("Failed to open file")

    width, height = img.size
    if width != 1500:
        ratio = 1500 / float(width)
        new_height = int((float(height) * float(ratio)))
        img = img.resize((1500, new_height), Image.LANCZOS)

    if img.mode == "RGBA":
        img = img.convert("RGB")
    if file_type == 'application/octet-stream':
        # If content type is generic, try to guess from the file name
        guessed_type = mimetypes.guess_type(file_name)[0]
        if guessed_type:
            file_type = guessed_type
        else:
            # If we can't guess, use the format from the opened image
            file_type = f"image/{img.format.lower()}"

    if '/' in file_type:
        image_format = file_type.split("/")[1].upper()
    else:
        # If file_type doesn't contain '/', use the format from the opened image
        image_format = img.format

    # Handle special cases
    if image_format == 'JPG':
        image_format = 'JPEG'
    elif image_format == 'WEBP':
        image_format = 'WebP'  # PIL uses 'WebP', not 'WEBP'

    # Fallback to JPEG if format is still not recognized
    if image_format not in ['JPEG', 'PNG', 'WebP', 'GIF']:
        image_format = 'JPEG'


    # image_format = file_type.split("/")[1].upper()





    img_io = io.BytesIO()
    img.save(img_io, format=image_format)
    img_io.seek(0)

    img_file = InMemoryUploadedFile(
        img_io,
        None,
        f"resized.{image_format.lower()}",
        f"image/{image_format.lower()}",
        img_io.getbuffer().nbytes,
        None,
    )
    
    image_instance.finished_at = timezone.now()
    
    upload_time = image_instance.finished_at - image_instance.uploaded_at
    upload_time_seconds = f"{upload_time.total_seconds():.1f} seconds"

    image_instance.upload_time = upload_time_seconds

    image_instance.image = img_file
    image_instance.status = 'completed'
    image_instance.save()
    
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    img_data_uri = f"data:image/{image_format.lower()};base64,{img_base64}"
    async_to_sync(channel_layer.group_send)(
        'upload_group',
        {
            'image': img_data_uri, 
            'type': 'send_upload_notification',
            'job_id': str(job_id),
            'status': 'completed',
            'message': f'Image {name} uploaded successfully.',
            'upload_time': upload_time_seconds
        }
    )
    
    
    
    