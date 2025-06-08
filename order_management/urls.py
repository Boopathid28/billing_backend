from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register('order', OrderViewSet, basename='order')
router.register('order-to-lot-details', OrderConvertToLotGetByIDViewSet, basename='order-to-lot-details')


urlpatterns = [
    # router urls included
    path('', include(router.urls)),

    path('order-for-list/', OrderForListView.as_view()),

    path('priority-list/', PriorityListView.as_view()),
    
    path('autogenerate-order-id/', GenerateOrderId.as_view()),
    path('order-list/', OrderListView.as_view()),
    path('order-item/', OrderItemView.as_view()),
    path('order-item/<str:pk>/', OrderItemView.as_view()),
    path('cancel-order/<int:pk>/', OrderCancelView.as_view()),
    # path('make-order-payments/', AddNewPaymentForOrderView.as_view()),
    path('assign-designer/', OrderIssueView.as_view()),
    path('recieve-items/', RecieveItemView.as_view()),

    # order file upload
    path('file-upload/', OrderFileUpload.as_view()),

    
    path('order-received-item/<str:pk>/', OrderReceivedItemListView.as_view()),
]