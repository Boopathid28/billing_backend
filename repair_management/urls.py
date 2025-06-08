from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register('order-repair-details',RepairOrderDetailsViewset,basename='order-repair-details')
router.register('repair-order-issue',RepairOrderIssueViewSet,basename='repair-order-issue')
router.register('delivery-bill',DeliveryBillViewSet,basename='delivery-bill')
router.register('repair-payment',RepairPaymentView,basename='repair-payment')


urlpatterns = [

    path('', include(router.urls)),

    #Repair For Details
    path('get-repair-for-dropdown/',GetRepairForDetails.as_view()),
    path('repair-type-dropdown/', GetRepairTypeDetails.as_view()),
    path('repair-order-list/', RepairOrderDetailsListView.as_view()),
    path('repair-order-id/', RepairOrderId.as_view()),
    path('repair-issue-id/', RepairIssueId.as_view()),
    path('repair-issue-list/',RepairIssueListView.as_view()),
    path('delivery-note-id/', DeliveryNoteId.as_view()),
    path('delivery-bill-list/', DeliveryBillListView.as_view()),
    path('repair-item-details/<str:pk>/', RepairItemDetailsList.as_view()),
    path('receive-item/', RecieveItemView.as_view()),
    path('repair-item-update/<int:pk>/', RepairItemUpdateAPIView.as_view()),
    path('repair-payment-list/',RepairPaymentListView.as_view()),
    

]