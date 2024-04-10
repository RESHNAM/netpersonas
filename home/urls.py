from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.index, name='index',),
    path('upload', views.upload, name='upload',),
    path('detailsave', views.detail_save, name='detail_save',),
    path("image-view", views.ImageListView.as_view(), name="image-view",),
    path("image-detail/<int:pk>", views.ImageDetailView.as_view(), name="image-detail",),
]

urlpatterns = format_suffix_patterns(urlpatterns)
