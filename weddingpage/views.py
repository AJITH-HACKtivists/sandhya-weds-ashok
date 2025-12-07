from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import GalleryModel
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from datetime import datetime
import boto3

# Create your views here.
class UploadsView(TemplateView):
    template_name='weddingpage/wedding_page.html'
    def get(self, request, *args, **kwargs):
          return super().get(request, *args, **kwargs)

class UploadImageAPI(APIView):
     def post(self, request, *args, **kwargs):
          image_files = request.FILES.getlist("Images")
          gallery_model_list=[]
          try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME

          except Exception as e:
            return Response(
                {"detail": f"S3 Client Initialization Error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
          files_response=[]
          base_url = (
                f"https://{bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com"
          )
          try:
                for f in image_files:
                    object_key = f"gallery/{f.name}-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
                    ExtraArgs={
                        "ACL": "public-read",
                        "ContentType": f.content_type,
                    }
                    s3_client.upload_fileobj(
                        f,
                        bucket_name,
                        object_key,
                        ExtraArgs={
                            "ContentType": f.content_type,
                        },
                    )
            
            # Construct the public URL (ensure your S3 bucket allows public read)
                    image_url = base_url+'/'+object_key
                    obj = GalleryModel(path=image_url)
                    gallery_model_list.append(
                       obj
                    )
                    files_response.append(
                    {
                        "path": object_key, # Store the relative S3 key if you prefer
                        "url": image_url,   # Store the full URL
                    }
                    )
                GalleryModel.objects.bulk_create(gallery_model_list)
                return Response(
                    {"files": files_response},
                 status=status.HTTP_201_CREATED,
                )   
          except Exception as e:
                 return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )