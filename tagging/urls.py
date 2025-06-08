from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('lot',LotViewset,basename='lot')
router.register('tag',TagEntryViewset,basename='tag')
router.register('tag-item',TagItemViewset,basename='tag-item')
router.register('single-tag',SingleTagViewset,basename='single-tag')
urlpatterns = [

    path('', include(router.urls)),

    #Lot APIS
    path('lot-id/',LotIDView.as_view()),
    path('lot-list/',LotListView.as_view()),
    path('lot-list/<int:branch>/',LotListView.as_view()),
    path('lot-item/<int:pk>/',LotItemDeleteView.as_view()),
    path('lot-stone/<int:pk>/',LotStoneDeleteView.as_view()),
    path('lot-stone-list/<int:pk>/',LotStoneList.as_view()),
    path('lot-diamond/<int:pk>/',LotDiamondDeleteView.as_view()),
    path('lot-diamond-list/<int:pk>/',LotDiamondList.as_view()),
    path('entry-type/',EntryTypeView.as_view()),
    path('weight-type/',WeightTypeView.as_view()),
    path('rate-type/',RateTypeView.as_view()),
    path('diamond-list/',DiamondListView.as_view()),

    #Tag APIs
    path('tag-number/<int:pk>/',TagNumberView.as_view()),
    path('tag-number/',TagNumberView.as_view()),
    path('tag-item-list/',TagItemByItem.as_view()),
    path('single-tag-update/<int:pk>/',SingleTagUpdate.as_view()),


    #Tag Entry List APIs
    path('tag-entry-list/',TagEntryListView.as_view()),
    path('tag-entry-list/<int:branch>/',TagEntryListView.as_view()),

    #Duplicate Tag Apis
    path('duplicate-tag/',DuplicateTagView.as_view()),


    #Stock List
    path('stock-list/',StockList.as_view()),
    path('huid-stock-list/',HUIDStockList.as_view()),

    path('itemtagcheck/',ItemtagCheckView.as_view()),

    path('tagitem-validation-view/<int:pk>/' , TagItemValidationView.as_view()),

    #Tag Item Gold
    path('tag-item-gold/<int:pk>/' , TagItemGOldViewset.as_view()),
    #Tag Item Silver
    path('tag-item-silver/<int:pk>/' , TagItemSilverViewset.as_view()),
    
    
    path('approval-gold-tag-item/',ApprovalGoldTagItemView.as_view()),
    path('approval-silver-tag-item/',ApprovalSilverTagItemView.as_view()),
    
]