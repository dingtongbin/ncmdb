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
"""
URL configuration for setting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views import NetworkEngineerUpload, check_user_role, get_statistics_data, get_user_info, change_password

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/statistics/', get_statistics_data, name='token_obtain_pair'),
    path('api/user_info/', get_user_info, name='token_obtain_pair'),
    path('api/change_password/', change_password, name='change_password'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/check-role/', check_user_role, name='check-user-role'),
    path('api/network-engineer/upload/', NetworkEngineerUpload.as_view(), name='network_engineer_upload'),
    path('api/repair/', include('repair.urls')),
    path('api/contact/', include('contact.urls')),
    path('api/file/', include('file_management.urls')),
    path('api/device/', include('device.urls')),
    path('api/integrated_facility/', include('integrated_facility.urls')),
    path('api/alert/', include('alert.urls')),
    path('api/inventory/', include('inventory.urls')),
    path('api/operation-affairs/', include('operation_affairs.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
