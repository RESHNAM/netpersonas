import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Image(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    cover = models.ImageField(upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
