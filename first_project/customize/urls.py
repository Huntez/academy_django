from django.urls import path
from . import views


urlpatterns = [
    path('upload/', views.upload_data, name='upload'),
    path('jsonupload/', views.json_upload, name='jsonupload'),
    path('textload/', views.text_load, name='textload'),
]

