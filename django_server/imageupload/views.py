
from .decorators import validate_image_in_request, validate_image_file_type, validate_images_in_request
from .models import ImageUpload
from .serializers import ImageUploadSerializer
from .tasks import process_and_save_image
from adrf.views import APIView as AsyncAPIView
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone
from PIL import Image
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
import io
import logging
import traceback
import uuid


class ListView(APIView):
    """
    API View to list all image uploads.
    """
    def get(self, request: Request) -> Response:
        """
        Handle GET requests to list all image uploads.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: A JSON response containing the list of image uploads.
        """
        image_uploads = ImageUpload.objects.all().order_by("-uploaded_at")
        serializer = ImageUploadSerializer(image_uploads, many=True)
        data = serializer.data
        response = Response(data, status=status.HTTP_200_OK)
        response["Content-Type"] = "application/json"
        return response
      

class UploadImageView(APIView):
    """
    API View to handle image upload.
    """
    @validate_image_in_request
    @validate_image_file_type
    def post(self, request: Request) -> Response:
        """
        Handle POST requests to upload an image.

        This method validates the image in the request, resizes it if necessary,
        converts it to the appropriate format, and saves it to the database.

        Args:
            request (Request): The HTTP request object containing the image file.

        Returns:
            Response: A JSON response indicating success or failure of the upload.
        """
        start_time = timezone.now()
        uploaded_image = request.FILES['image']
        file_size = uploaded_image.size
        file_type = uploaded_image.content_type
        file_name = uploaded_image.name

        try:
            img = Image.open(uploaded_image)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
   
        width, height = img.size
        if width != 1500:
            ratio = 1500 / float(width)
            new_height = int((float(height) * float(ratio)))
            img = img.resize((1500, new_height), Image.LANCZOS)  # Updated to use LANCZOS

        if img.mode == "RGBA":
            img = img.convert("RGB")

        image_format = file_type.split("/")[1].upper()
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
        job_id = f"__;;{file_name}"

        # Initialize image instance
        image_instance = ImageUpload(
            image=img_file, 
            size=file_size, 
            type=file_type, 
            name=file_name, 
            job_id=job_id,
            status="completed" 
        )

        # Set finished_at to current time
        image_instance.finished_at = timezone.now()

        # Save instance first to update finished_at
        image_instance.save()

        # Calculate upload time
        upload_time = image_instance.finished_at - start_time
        image_instance.upload_time = f"{upload_time.total_seconds():.1f} seconds"

        # Update and save instance with upload_time
        image_instance.save()

        return Response({"message": "Image uploaded successfully"}, status=status.HTTP_200_OK)
      
        
class AsyncUploadImageView(AsyncAPIView):
    """
    API View to handle asynchronous image upload.
    """
    @validate_images_in_request
    async def post(self, request: Request) -> Response:
      """
      Handle POST requests to upload images asynchronously.

      This method validates the images in the request, saves each image instance
      with a 'processing' status, and triggers a background task to process and save
      the image.

      Args:
          request (Request): The HTTP request object containing the image files.

      Returns:
          Response: A JSON response indicating the initiation of the image uploads.
      """
      try:
          images = request.FILES.getlist("images")
          for index, uploaded_image in enumerate(images):
              file_size = uploaded_image.size
              file_type = uploaded_image.content_type
              file_name = uploaded_image.name

              # Convert uploaded_image to bytes
              image_bytes = await sync_to_async(uploaded_image.read)()

              if ';;' in file_name:
                  job_id, name = file_name.split(';;')
              else:
                  job_id = str(uuid.uuid4())
                  name = file_name
                  file_name = f"{job_id};;{name}"
              
              image_instance = ImageUpload(
                  size=file_size,
                  type=file_type,
                  name=name,
                  job_id=job_id,
                  status='processing'
              )
              await database_sync_to_async(image_instance.save)()
              process_and_save_image.delay(image_bytes, file_name, file_size, file_type, image_instance.id)

      except Exception as e:
          print('AsyncUploadImageView Exception', e)
          logging.error(f'Error AsyncUploadImageView: {e}\n{traceback.format_exc()}')

          return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

      return Response(
          {"message": "Images upload initiated"}, status=status.HTTP_200_OK
      )
      
      