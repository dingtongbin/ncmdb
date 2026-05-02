# filem/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.list_directory, name='file-list'),
    path('upload/', views.upload_files, name='file-upload'),
    path('folder/create/', views.create_folder, name='folder-create'),
    path('rename/', views.rename_item, name='item-rename'),
    path('delete/', views.delete_item, name='item-delete'),
    path('preview/', views.preview_file, name='file-preview'),
    path('download/', views.download_file, name='file-download'),
]
