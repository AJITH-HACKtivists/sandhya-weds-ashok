from django.contrib import admin
from django.urls import path
from .views import UploadsView
from .views import UploadImageAPI

urlpatterns = [
    path("uploads/", UploadsView.as_view()),
    path("upload-api-url/", UploadImageAPI.as_view(), name='image-upload-url')
]
