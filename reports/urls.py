from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    # router urls included
    path('', include(router.urls)),

    path('dailystock-item-list/', DailyStockItemListView.as_view()),
    path('dailystock-subitem-list/', DailyStockSubItemListView.as_view()),
    path('dailystock-metal-list/', DailyStockMetalListView.as_view()),
    path('dailystock-purity-list/', DailyStockPurityListView.as_view()),
    path('dailystock-designer-list/', DailyStockDesignerListView.as_view()),

    path('metal-wise-sale-report/',MetalWiseSalesReport.as_view()),
    path('purity-wise-sale-report/',PurityWiseSaleReport.as_view()),
    path('item-wise-sale-report/',ItemWiseSaleReport.as_view()),
    path('sub-item-wise-sale-report/',SubItemWiseSaleReport.as_view()),
    path('customer-sale-report/', CustomerWiseSaleReport.as_view()),
    path('vendor-wise-sale-report/',VendorWiseSalesReport.as_view()),

    path('estimation-report-list/', EstimationReportListView.as_view()),

    path('suspense-redeeme-report/',SuspenseRedeemReport.as_view()),
    path('suspense-repayment-report/',SuspenseRepaymentReport.as_view()),
    path('suspense-pending-report/',SuspensePendingReport.as_view()),

    path('item-wise-purchase/',ItemwisePurchaseListView.as_view()),
    path('vendor-wise-purchase/',VendorwisePurchaseListView.as_view()),

    path('item-wise-lot-report/',ItemwiseLotListView.as_view()),
    ####################### OLD APIS ########################333
    path('billing-report-list/', BillingReportListView.as_view()),
    path('billing-backup-report-list/', BillingBackupReportListView.as_view()),
    path('itemreport-list/', TagItemListView.as_view()),
    path('tagged-itemwise-list/', TaggedItemWiseListView.as_view()),
    path('estimation-gst-list/', EstimationGSTReportView.as_view()),
    path('billing-gst-list/', BillingGSTReportView.as_view()),
    
    path('sale-details-report/', SalesDetailsReport.as_view()),
    path('sale-return-report/', SaleReturnReport.as_view()),
    path('stock-summary-report/', StockSummaryReport.as_view()),
    path('tagwise-stock-report/', TagWiseStockReport.as_view()),
    path('lot-report/', LotReport.as_view()),
    path('purchase-report/', PurchaseReport.as_view()),
    path('vendor-purchase-report/', VendorWisePurchaseReport.as_view()),
    path('item-purchase-report/', ItemWisePurchaseReport.as_view()),
    path('old-purchase-report/', OldPurchaseReport.as_view()),
    path('vendor-lot-report/', VendorWiseLotReport.as_view()),
    path('customer-repair-issue-report/', CustomerRepairIssueReport.as_view()),
    path('vendor-repair-issue-report/', VendorRepairIssueReport.as_view()),
    path('misc-billing-report/', MiscDetailsReport.as_view()),
    path('approval-issue-report/', ApprovalIssueReport.as_view()),
    path('item-wise-monthly-salereport/', ItemWiseMonthlySalesReport.as_view()),
    #Common payment report
    path('common-payment-report/', CommonPaymentReportListView.as_view()),
    #Sales incentive report
    path('sales-incentivepercent-report/', SalesIncentivePercentReportView.as_view()),
    path('sales-incentiveamount-report/', SalesIncentiveAmountReportView.as_view()),
    path('cash-counter-report/', CashCounterReport.as_view()),
    



]
