from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register('customer', CustomerViewSet, basename='customer')
router.register('customer-group', CustomerGroupView, basename='customer-group')

urlpatterns = [
    # router urls included
    path('', include(router.urls)),

    # Customer APIs
    path('customer-list/', CustomerList.as_view()),
    path('customer-list/<int:branch>/', CustomerList.as_view()),
    path('customer-group-list/', CustomerGroupList.as_view()),  
    path('customer-group-status/<int:pk>/', CustomerGroupStatusView.as_view()),  
    
    path('shop-list/', ShopListView.as_view()),  
    path('shop-list/<int:customer_group>/', ShopListView.as_view()),  

    path('customer-mobile-search/<str:phone>/', CustomerMobileNumberAPIView.as_view()),
    
    path('customer-ledger-list/', CustomerLedgerListView.as_view()),  
]