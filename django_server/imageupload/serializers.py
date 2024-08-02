# serializers.py
from rest_framework import serializers
from .models import ImageUpload

class ImageUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for the ImageUpload model.

    This serializer is responsible for converting ImageUpload model instances
    to JSON representations and vice versa. It includes all fields from the
    ImageUpload model.

    Attributes:
        model (Model): The Django model class being serialized.
        fields (str): Specifies which model fields to include in the serialized output.
    """
    class Meta:
        model = ImageUpload
        fields = "__all__" 
