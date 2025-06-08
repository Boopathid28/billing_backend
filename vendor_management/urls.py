from django.urls import path,include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('vendor-discount',VendorDiscountView,basename='vendor-discount')
router.register('vendor-payment',VendorPaymentView,basename='vendor-payment')


urlpatterns = [
    path('', include(router.urls)),
    path('vendor-discount-list/', VendorDiscountList.as_view()),
    path('vendor-payment-list/', VendorPaymentListView.as_view()),
    path('vendor-ledger-list/', VendorLedgerListView.as_view()),
    path('vendor-payment-details/<int:vendor>/', VendorPaymentDetailsView.as_view()),
    path('vendor-ledger-list-export/', VendorLedgerListExcelView.as_view()),
    path('vendor-payment-list-export/', VendorPaymentListExcelView.as_view()),

]