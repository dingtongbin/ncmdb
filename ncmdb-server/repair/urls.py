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
# repair/urls.py
from django.urls import path

from . import views

urlpatterns = [
    # 工单管理 API（新版）
    path('work-order/create/', views.create_work_order, name='create-work-order'),
    path('work-order/my-list/', views.get_my_work_orders, name='get-my-work-orders'),
    path('work-order/<int:id>/', views.get_work_order_detail, name='work-order-detail'),
    path('work-order/<int:id>/evaluation/', views.submit_evaluation, name='submit-evaluation'),
    # 网络工程师专用 API
    path('engineer/work-orders/', views.get_engineer_work_orders, name='engineer-work-orders'),
    path('engineer/work-order/<int:id>/accept/', views.accept_work_order, name='accept-work-order'),
    path('engineer/work-order/<int:id>/submit-result/', views.submit_work_order_result,
         name='submit-work-order-result'),

]
