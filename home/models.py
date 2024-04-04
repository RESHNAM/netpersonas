import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def make_image_path(pathfolder):
    image_path = os.path.join(settings.MEDIA_ROOT, 'users', pathfolder, 'images')
    return image_path


# Create your models here.
class Image(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    cover = models.ImageField(upload_to=make_image_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
