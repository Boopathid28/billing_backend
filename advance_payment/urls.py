from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register('advancepayment', AdvancePaymentViewSet, basename='advancepayment')

urlpatterns = [
    # router urls included
    path('', include(router.urls)),

    # Advance Purpose APIs
    path('advance-purpose/', AdvancePurposeView.as_view()),
    
    # Advance Payment APIs
    path('advance-payment-list/', AdvancePaymentList.as_view()),
    path('advance-payment-list/<int:branch>/', AdvancePaymentList.as_view()),
    path('advance-number-autogenerate/', AdvanceNumberAutoGenerate.as_view()),
    path('advance-search/<str:pk>/',AdvanceSearchView.as_view()),
]