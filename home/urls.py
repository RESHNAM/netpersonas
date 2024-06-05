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

    #vance ai urls
    path('vance-upload-image/<int:pk>/', views.enhance_upload, name='enhance-upload-image',),
    path('vance-transform-image/<uuid:uid>/', views.image_transform, name='transform-image',),
    path('progress/<uuid:trans_id>/', views.check_progress, name='progress-check',),
    path('download/<uuid:trans_id>/', views.download_image, name='download-check',),

]

urlpatterns = format_suffix_patterns(urlpatterns)
