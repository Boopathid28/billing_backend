from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register('purchasetype', PurchaseTypeViewSet, basename='PurchaseType')
router.register('purchaseentry', PurchaseViewset, basename='PurchaseType')

#New purchase order API
router.register('new-purchase', NewPurchaseViewset, basename='New Purchase Order')

urlpatterns = [
    # router urls included
    path('', include(router.urls)),

    # PurchaseType APIs
    path('purchaseorder-id/', PurchaseorderIDView.as_view()),
    path('purchasetype-list/', PurchaseTypeList.as_view()),
    path('purchasetax-list/<int:pk>/', PurchaseTaxList.as_view()),
    path('purchaseentry-list/', PurchaseEntryListView.as_view()), #Purchase order based on purchase type
    path('billing/<str:billno>/', BillingAPIView.as_view()), 
    path('billing-list/<int:branch>/', BillingListView.as_view()), 
    path('billing-list/', BillingListView.as_view()),
    path('calculate/', CalculateView.as_view()), 
    
    #New purchase order API
    path('newpurchase-id/', NewPurchaseorderIDView.as_view()),
    # path('newpurchase-list/', NewPurchaseListView.as_view()),
    path('newpurchase-list/', NewPurchaseEntryListView.as_view()),


    

    # Vendor Payment API
    path('vendorpayment-id/', NewPurchaseTransactionIDView.as_view()),    
    path('getvendordetail/<int:pk>/<int:type>/',VendorDetailView.as_view()),
    path('metal-rate-cut/', MetalRatecutView.as_view()), 
    path('cash-rate-cut/', CashRatecutView.as_view()), 
    path('amount-rate-cut/', AmountsettleView.as_view()), 
    # path('vendor-payment/', VendorpaymentView.as_view()),
    path('vendor-list/', VendorPaymentListView.as_view()),
    path('item-list/', ItemListView.as_view()),

    path('stone-delete/<int:pk>/', StoneDeleteView.as_view()),
    path('diamond-delete/<int:pk>/', DiamondDeleteView.as_view()),
    path('item-delete/<int:pk>/', ItemDeleteView.as_view())
 ]