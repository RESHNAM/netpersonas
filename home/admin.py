from django.contrib import admin

from .models import Image, Feedback

# Register your models here.
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("author","name","cover","created_at","updated_at")

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("name","email","subject","message","date")
