from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [

    path('', include(router.urls)),

    #Repair For Details
    path('payment-method-list/',PaymentMethodList.as_view()),
    path('payment-provider-list/<int:pk>/',PaymentProviderList.as_view()),
    path('payment-provider-list/',PaymentProviderList.as_view()),
    path('payment-view/',PaymentView.as_view()),
    path('payment-module-list/',PaymentModuleListView.as_view()),
    
]