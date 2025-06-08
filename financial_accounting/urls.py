from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [

    path('', include(router.urls)),

    #Repair For Details
    path('ledger-list/',LedgerListView.as_view()),
    path('customer-payment-list/<int:customer>/<int:type>/',CustomerPaymentListView.as_view()),
    
]