from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.index, name='index',),
    path('upload', views.upload, name='upload',),
    path('detailsave', views.detail_save, name='detail_save',),
    path('process-image/<int:pk>/', views.Denoidebluenha, name='process-image',),
    path('contactus', views.feedback, name='feedback',),
    path('api/new-user', views.NewUserList.as_view(), name='new-user'),
    path('api/users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('api/image-view', views.ImageListView.as_view(), name='image-view'),
    path('api/image-detail/<int:pk>/', views.ImageDetailView.as_view(), name='image-detail'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework_api')),

    path('aiimage/<int:pk>/', views.ai_image_process, name='aiimage',),
    path('backgroundcustom/<int:pk>/', views.background_customisation_process, name='backgroundcustom',),
    path('facerecognition/<int:pk>/', views.face_recognition_process, name='facerecognition',),

    
]

urlpatterns = format_suffix_patterns(urlpatterns)
