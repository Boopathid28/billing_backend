from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register('metal', MetalViewSet, basename='metal')
router.register('purity', PurityViewSet, basename='purity')
# router.register('metal-rates', MetalRateViewSet, basename='metal-rates')
router.register('tax',TaxDetailsViewset,basename='tax')
router.register('shape',ShapeDetailsviewset,basename='shape')
router.register('cut',CutDetailsViewset,basename='cut')
router.register('color',ColourDetailViewset,basename='color')
router.register('clarity',ClarityDetailsViewset,basename='clarity')
router.register('cent-group',CentGroupViewset,basename='cent-group')
router.register('tag-type',TagTypeViewset,basename='tag-type')
router.register('stone',StoneDetailsViewset,basename='stone')
router.register('carat-rate',CaratRateViewset,basename='carat-rate')
router.register('range-stock',RangeStockViewset,basename='range-stock')
router.register('repair-type',RepairTypeView,basename='repair-type')
router.register('voucher-type',VoucherTypeViewSet,basename='voucher-type')
router.register('gift-voucher',GiftVoucherViewSet,basename='gift-voucher')
router.register('old-metal-rate',OldMetalRateViewSet,basename='old-metal-rate')
router.register('tax-audit-details',TaxDetailsAuditViewSet,basename='tax-audit-details')
router.register('cash-counter',CashCounterViewSet,basename='cash-counter')

urlpatterns = [
    # router urls included
    path('', include(router.urls)),

    # Metal APIs
    path('metal-list/', MetalList.as_view()),
    path('change-metal-status/<int:pk>/', MetalStatus.as_view()),

    # Purity APIs
    path('purity-list/<int:pk>/', PurityList.as_view()),
    path('purity-list/', PurityList.as_view()),
    path('change-purity-status/<int:pk>/', PurityStatus.as_view()),
    path('change-purity-visible/<int:pk>/', PurityVisible.as_view()),
    

    # MetalRate APIs
    # path('metal-rates-list/', MetalRateList.as_view()),
    # path('today-metal-rate/', TodayMetalrate.as_view()),
    # path('display-metal-rate/', DisplayMetalrate.as_view()),

    #Taxdetails APIs
    path('tax-list/',TaxDetailList.as_view()),
    path('change-tax-status/<int:pk>/',TaxDetailStatusView.as_view()),

    #shape detail APIs
    path('shape-list/',ShapeDetailListView.as_view()),
    path('change-shape-status/<int:pk>/',ShapeStatusView.as_view()),

    #Cut Details APIs
    path('cut-list/',CutListView.as_view()),
    path('change-cut-status/<int:pk>/',CutStatusView.as_view()),

    #Colour Details APIs
    path('change-color-status/<int:pk>/',ColourStatusView.as_view()),
    path('color-list/',ColourListView.as_view()),

    #Clarity Details APIs
    path('clarity-list/',ClarityListView.as_view()),
    path('change-clarity-status/<int:pk>/',ClarityStatusView.as_view()),

    #Cent Group APIs
    path('change-cent-group-status/<int:pk>/',CentGroupStatusView.as_view()),
    path('cent-group-list/',CentGroupListView.as_view()),

    #Tag Type APIs
    path('change-tag-type-status/<int:pk>/',TagTypeStatusView.as_view()),
    path('tag-type-list/',TagTypeListView.as_view()),

    #Stone APIs
    path('stone-list/',StoneListView.as_view()),
    path('change-stone-status/<int:pk>/',StoneStatusView.as_view()),

    #Carat Rate APIs
    path('carat-rate-status/<int:pk>/',CaratRateStatusView.as_view()),
    path('carat-rate-list/',CaratRateListView.as_view()),

    #Range Stock APIs
    path('change-range-stock-status/<int:pk>/',RangeStockStatusView.as_view()),
    path('range-stock-list/',RangeStockListView.as_view()),

    path('metal-based-purity/<int:pk>/', MetalbasedPurityView.as_view()),    

    # path('display-metal-rate/', DisplayMetalrate.as_view()),

    #Repair Type
    path('repair-type-status/<int:pk>/', RepairTypeStatusView.as_view()),
    path('repair-type-list/', RepairTypeListView.as_view()),


    path('range-stock-report/<int:pk>/',RangeStockReport.as_view()),

    #Voucher Type
    path('voucher-type-status/<int:pk>/', VoucherTypeStatusView.as_view()),
    path('voucher-type-list/', VoucherTypeListView.as_view()),

    #UPI Type
    path('gift-voucher-status/<int:pk>/', GiftVoucherStatusView.as_view()),
    path('gift-voucher-list/', GiftVoucherListView.as_view()),
    path('get-gift-voucher/<str:voucher_no>/', GiftVoucherDetailsView.as_view()),

    path('gst-list/', GSTListView.as_view()),

    path('metal-rates/', NewMetalRateListView.as_view()),   #Create metal rate
    path('metal-rates-list/', NewMetalRateList.as_view()),  #metal rate list
    path('display-metal-rate/', NewDisplayMetalRate.as_view()),  #display metal rate
    path('today-metal-rate/', NewDisplayMetalRate.as_view()),   #today metal rate

    # OLD METAL RATE LIST
    path('old-metal-rate-list/<int:metal>/', OldMetalRateList.as_view()),
    path('old-metal-rate-list/', OldMetalRateList.as_view()),

    # TAX AUDIT DETAILS LIST
    path('tax-audit-list/', TaxAuditDetailsList.as_view()),

    # CASH COUNTER
    path('cash-counter-list/', CashCounterList.as_view()),
    path('cash-counter-status-change/<int:pk>/', CashCounterStatusView.as_view()),
    path('cash-counter-check/', CashCounterCheckView.as_view()),
    
    
]