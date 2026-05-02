# Copyright 2026 dingtongbin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
