from django.urls import path,include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('old-gold',OldGoldBillingView,basename='old-gold')



urlpatterns = [
    path('', include(router.urls)),
    path('old-gold-list/', OldGoldBillListView.as_view()),
    path('old-gold-search/<str:pk>/', OldGoldSerachView.as_view()),
    path('oldgold-number-generate/', OldgoldNumberGenerateAPIView.as_view()),
    
    
]