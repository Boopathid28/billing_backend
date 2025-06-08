from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('approval-type', ApprovalTypeViewSet, basename='approval-type')
router.register('approval-rule', ApprovalRuleViewSet, basename='approval-rule')

urlpatterns = [
      # router urls included
    path('', include(router.urls)),

    # Approval Type APIs
    path('approval-type-list/', ApprovalTypeList.as_view()),
    path('approval-type-status/<int:pk>/', ApprovalTypeStatus.as_view()),

    # Approval Rule APIs
    path('approval-rule-list/', ApprovalRuleList.as_view()),
    path('approval-rule-status/<int:pk>/', ApprovalRuleStatus.as_view()),
   
]