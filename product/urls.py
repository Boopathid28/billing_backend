from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register('item',ItemDetailViewset,basename='item')
router.register('sub-item',SubItemViewset,basename='sub-item')

urlpatterns = [

    path('', include(router.urls)),


    #StockType APIs
    path('stock-type/',StockTypeView.as_view()),

    #Calculation Type APIs
    path('calculation-type/',CalculationTypeView.as_view()),

    #Measurement Type APIs
    path('measurement-type/',MeasurementTypeView.as_view()),

    #Weight Type APIs
    path('weight-type/',WeightTypeView.as_view()),

    #Item APIs
    path('change-item-status/<int:pk>/',ItemStatusView.as_view()),
    path('item-list/',ItemListView.as_view()),
    path('item-metal/',ItemByMetal.as_view()),
    path('item-metal-stock/',ItemByMetalStock.as_view()),


    #Item Image APIs
    path('item-image-upload/',ItemImageUpload.as_view()),
    path('item-image-upload/<str:file>/',ItemImageUpload.as_view()),

    #Item ID APIs
    path('item-id/',ItemIdview.as_view()),

    #SubItem APIs

    path('change-sub-item-status/<int:pk>/',SubItemStatusView.as_view()),
    path('sub-item-list/<int:pk>/',SubItemList.as_view()),
    path('sub-item-list/',SubItemList.as_view()),
    path('sub-item-item-calc/',SubItemByItemCalculation.as_view()),
    path('sub-item-item/',SubItemByItem.as_view()),
    path('sub-item-metal-stock-calc/',SubItemByMetalStockCalc.as_view()),
    path('item-metal-stock-calc/',ItemByMetalStockCalc.as_view()),

    #SubItem ID APIs
    path('sub-item-id/',SubItemIdview.as_view()),

    #SubItemImage Upload

    path('sub-item-image-upload/',SubItemImageUpload.as_view()),
    path('sub-item-image-upload/<str:file>/',SubItemImageUpload.as_view()),

]