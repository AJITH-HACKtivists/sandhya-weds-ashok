from django.db import models

# Create your models here.
class GalleryModel(models.Model):
    id=models.BigAutoField(primary_key=True)
    path=models.TextField(null=False, blank=False)
    created_date=models.DateTimeField(auto_now_add=True)