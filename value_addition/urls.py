from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register('value-addition-customer',ValueAdditionCustomerViewset,basename='value-addition-customer')
router.register('value-addition-designer',ValueAdditionDesignerView,basename='value-addition-designer')

urlpatterns = [
    # router urls included
    path('', include(router.urls)),
    path('value-addition-customer-list/', ValueAdditionCustomerList.as_view()),
    path('value-addition-designer-list/', ValueAdditionDesignerList.as_view()),
    path('sub-item-details/', SubitemDetailsAPIView.as_view()),
    path('tag-value/', TagValueView.as_view()),
    path('purchase-value/', PurchaseTagValueView.as_view()),
    path('flatwastage-type/', FlatWastageTypeView.as_view()),
    path('valueaddition-designer-details/', ValueadditionDesignerDetailsView.as_view()),

]