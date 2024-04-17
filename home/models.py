import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# from django.contrib.gis.db import models as modelz

# Create your models here.
class Image(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    cover = models.ImageField(upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Feedback(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the sender")
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Feedback"

    def __str__(self):
        return self.name + "-" +  self.email
    
# class Location(modelz.Model):
#     name = modelz.CharField(max_length=50, default = 'Unknown location')
#     mpoint = modelz.PointField()

#     def __str__(self):
#         return self.name
