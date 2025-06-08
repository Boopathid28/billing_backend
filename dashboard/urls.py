from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    path('dashboard-count/',DashboardCountView.as_view()),
    path('total-payment/',TotalPaymentView.as_view()),
    path('metal_wise_sales/',MetalWiseSalesView.as_view()),
    path('item-stock-list/',ItemWiseStockListView.as_view()),
    path('purchase-list/',PurchaseListView.as_view()),
    path('billing-list/',BillingListView.as_view()),
    path('salesvspurchase-list/',SalesandPurchaseListView.as_view()),
    path('vendorwise-list/',VendorListView.as_view()),
    
    
    
]

    
