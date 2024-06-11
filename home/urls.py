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

    #vance ai urls for upload
    path('enhance-upload-image/<int:pk>/', views.enhance_upload, name='enhance-upload-image',),
    path('backcustom-upload-image/<int:pk>/', views.backcustom_upload, name='back-custom-image',),
    path('scale-upload-image/<int:pk>/', views.scale_image_upload, name='scale-image',),
    path('facialrec-upload-image/<int:pk>/', views.facialrec_image_upload, name='facial-recognition-image',),
    path('styletransfer-upload-image/<int:pk>/', views.styletransfer_image_upload, name='style-transfer-image',),
    path('colourcorr-upload-image/<int:pk>/', views.colourcorrection_image_upload, name='colour-correction-image',),
    path('retouchalgo-upload-image/<int:pk>/', views.faceretouch_image_upload, name='face-retouch-algo-image',),
    path('lightadjust-upload-image/<int:pk>/', views.lightadjust_image_upload, name='light-adjust-image',),
    path('brandelement-upload-image/<int:pk>/', views.brandelement_image_upload, name='brand-element-image',),
    path('customfilter-upload-image/<int:pk>/', views.customfilter_image_upload, name='custom-filter-image',),
    
    #vance ai urls for transformation
    path('vance-transform-image/<uuid:uid>/', views.image_transform_enhance, name='transform-image',),
    path('progress/<uuid:trans_id>/', views.check_progress, name='progress-check',),

    #vance ai urls for download
    path('download/<uuid:trans_id>/', views.download_image, name='download-check',),

]

urlpatterns = format_suffix_patterns(urlpatterns)
