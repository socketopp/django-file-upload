from django.db import models
import uuid

class ImageUpload(models.Model):
    """
    Model representing an uploaded image and its metadata.

    This model stores information about uploaded images, including the image file itself,
    upload timestamps, processing status, and other relevant metadata.

    Attributes:
        id (UUIDField): Unique identifier for the image upload.
        image (ImageField): The uploaded image file.
        uploaded_at (DateTimeField): Timestamp when the image was uploaded.
        finished_at (DateTimeField): Timestamp when processing was completed (nullable).
        upload_time (CharField): String representation of the upload duration.
        size (PositiveIntegerField): Size of the image file in bytes.
        type (CharField): MIME type of the image file.
        name (CharField): Original filename of the uploaded image.
        job_id (CharField): Unique identifier for the upload job (nullable).
        status (CharField): Current status of the image processing.

    The status field can have the following values:
        - 'pending': Upload initiated but not yet processed.
        - 'processing': Image is currently being processed.
        - 'completed': Image processing has been successfully completed.
        - 'aborted': Image processing was aborted. (not implemented)
        - 'error': An error occurred during processing.

    Methods:
        __str__: Returns the name of the image as a string representation.
    """
    class Meta:
      db_table = 'images'

    STATUS_CHOICES = [
      ('pending', 'Pending'),
      ('processing', 'Processing'),
      ('completed', 'Completed'),
      ('aborted', 'Aborted'),
      ('error', 'Error')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to="images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    upload_time = models.CharField(max_length=50, null=True, blank=True)  
    size = models.PositiveIntegerField(default=0)  
    type = models.CharField(max_length=50, default="unknown")  
    name = models.CharField(
        max_length=255, default="default_image_name.jpg"
    )  
    job_id = models.CharField(max_length=256, unique=True, null=True, blank=True)
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, default='processing')

    def __str__(self):
        return self.name
