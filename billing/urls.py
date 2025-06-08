from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('sale-bill', BillingView, basename='sale-bill')

urlpatterns = [
    # router urls included
    path('', include(router.urls)),

    #Estimation APIs
    path('estimation-billing/', EstimationAPIView.as_view()),
    #Bill Type APIs
    path('bill-type/', BillTypeList.as_view()),
    
    path('estimation-without-stock/',EstimationWithoutStockReduceView.as_view()),
    path('estimation-billing/<int:pk>/', EstimationAPIView.as_view()),
    path('estimation-billing/<int:pk>/<int:branch>/', EstimationAPIView.as_view()),
    path('estimation-number-autogenerate/', EstimationNumberGenerateAPIView.as_view()),
    path('estimate-number-search/', EstimateNumberSearch.as_view()),
    path('estimation-list/',EstimationListView.as_view()),
    path('estimation-list/<int:branch>/',EstimationListView.as_view()),
    path('estimation-edit/<int:pk>/', EstimationEditView.as_view()),

    path('estimation-details-approval-list/', EstimationDetailsApprovalView.as_view()),
    path('estimation-status-approval/<int:pk>/', EstimationStatusApprovalView.as_view()),
    path('estimate-details-for-approved/<int:branch>/',GetEstimateNoForApprovedOnly.as_view()),
    
    path('gold-estimation-number/', GoldEstimationnumberView.as_view()),
    path('silver-estimation-number/', SilverEstimationnumberView.as_view()),
    
    #Biiling APIs
    path('sale-bill-payment/',BillPaymentView.as_view()),
    path('sale-bill-list/',BillingListView.as_view()),

    # path('sale-bill/',BillingView.as_view()),
    # path('sale-bill/<int:pk>/',BillingView.as_view()),
    path('sale-bill-without-stock/',BillingWithOutStockReduceView.as_view()),
   

    path('bill-number/',BillnumberView.as_view()),
    path('silver-bill-number/',SilverBillnumberView.as_view()),

    path('oldgold-number-autogenerate/',OldgoldNumberGenerateAPIView.as_view()),
    path('oldgold-number-bill/',OldgoldNumberForBillAPIView.as_view()),
    path('sale-bill-update/<int:pk>/',BillingReviseView.as_view()),

    # Misc Issue APIs
    path('generate-misc-id/', GenerateMiscIssueId.as_view()),
    path('create-misc/', CreateMiscBillingView.as_view()),

    path('metal-estimation-list/', MetalEstimationListView.as_view()),
    path('test-view/', TestView.as_view()),

    path('tag-item-list/', TagItemListView.as_view()),
    path('staff-id-search/<str:staff_id>/', StaffIdCheckAPIView.as_view()),

    
    path('estimation-tag-item-list/', EstimationItemListAPIView.as_view()),
    path('estimation-list-by-customer/<int:pk>/', GetEstimationListByCustomerView.as_view()),
    path('estimation-multiselect-list/', EstimationMultiSelectAPIView.as_view()),
    
]   