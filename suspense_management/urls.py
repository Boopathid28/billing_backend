from django.urls import path,include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('suspense',SuspenseView,basename='suspense')

urlpatterns = [
    path('', include(router.urls)),
    
    path('suspense-number-generate/', SuspenseNumberView.as_view()),
    path('suspense-paymentid-generate/', SuspensePaymentIdGenerateView.as_view()),
    path('suspense-payment/', SuspensePaymentView.as_view()),
    path('suspense-list/', SuspenseListView.as_view()),
    path('suspense-search/<str:pk>/', SuspenseNumberSearch.as_view()),

]