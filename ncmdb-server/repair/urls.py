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
