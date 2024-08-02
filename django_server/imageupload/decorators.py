# decorators.py
import mimetypes
from rest_framework.response import Response
from rest_framework import status
from functools import wraps
from typing import Callable, Awaitable
from django.http import HttpRequest
from rest_framework.request import Request

def validate_image_in_request(func: Callable[..., Response]) -> Callable[..., Response]:
    """
    Decorator to validate the presence of an image file in the request.

    Args:
        func (Callable[..., Response]): The view function to be decorated.

    Returns:
        Callable[..., Response]: The wrapped function.

    Raises:
        Response: HTTP 400 response if no image file is provided.
    """
    @wraps(func)
    def wrapper(self, request: HttpRequest, *args, **kwargs) -> Response:
        if "image" not in request.FILES:
            return Response(
                {"error": "No image file provided"}, status=status.HTTP_400_BAD_REQUEST
            )
        return func(self, request, *args, **kwargs)
    return wrapper

def validate_images_in_request(func: Callable[..., Awaitable[Response]]) -> Callable[..., Awaitable[Response]]:
    """
    Decorator to validate the presence of image files in the request for async views.

    Args:
        func (Callable[..., Awaitable[Response]]): The async view function to be decorated.

    Returns:
        Callable[..., Awaitable[Response]]: The wrapped async function.

    Raises:
        Response: HTTP 400 response if no images are provided.
    """
    @wraps(func)
    async def wrapper(self, request: Request, *args, **kwargs) -> Response:
        if "images" not in request.FILES:
            return Response(
                {"error": "No images provided"}, status=status.HTTP_400_BAD_REQUEST
            )
        return await func(self, request, *args, **kwargs)
    return wrapper

def validate_image_file_type(func: Callable[..., Response]) -> Callable[..., Response]:
    """
    Decorator to validate the file type of the uploaded image.

    Args:
        func (Callable[..., Response]): The view function to be decorated.

    Returns:
        Callable[..., Response]: The wrapped function.

    Raises:
        Response: HTTP 400 response if the file type is not an image.
    """
    # @wraps(func)
    # def wrapper(self, request: HttpRequest, *args, **kwargs) -> Response:
    #     uploaded_image = request.FILES["image"]
    #     file_type = uploaded_image.content_type
    #     if not file_type.startswith("image/"):
    #         return Response(
    #             {"error": "Invalid file type"}, status=status.HTTP_400_BAD_REQUEST
    #         )
    #     return func(self, request, *args, **kwargs)
    # return wrapper
    @wraps(func)
    def wrapper(self, request: HttpRequest, *args, **kwargs) -> Response:
        uploaded_image = request.FILES["image"]
        file_type = uploaded_image.content_type

        # If content_type is not specified or is generic, try to guess from the filename
        if not file_type or file_type == 'application/octet-stream':
            guessed_type = mimetypes.guess_type(uploaded_image.name)[0]
            if guessed_type:
                file_type = guessed_type
            else:
                # If we can't guess, we'll assume it's not an image
                return Response(
                    {"error": "Unable to determine file type"}, status=status.HTTP_400_BAD_REQUEST
                )

        if not file_type.startswith("image/"):
            return Response(
                {"error": "Invalid file type"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add the guessed file_type to the request for use in the view
        request.FILES["image"].content_type = file_type
        
        return func(self, request, *args, **kwargs)
    return wrapper

