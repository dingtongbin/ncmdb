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
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from inventory.views import InventoryItemModelViewSet, InventoryRecordViewSet

router = DefaultRouter()
router.register(r'item', InventoryItemModelViewSet, basename='inventory-item')
router.register(r'record', InventoryRecordViewSet, basename='inventory-record')

urlpatterns = [
    path('', include(router.urls)),
]
