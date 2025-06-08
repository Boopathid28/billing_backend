from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register('tansferitem',TransferItemViewset,basename='tansferitem')
router.register('receiveditem',ReceiveitemViewset,basename='receiveditem')
router.register('returnitem',ReturnItemViewset,basename='returnitem')
router.register('approvetransferitem',ApproveTransferItemViewset,basename='approvetransferitem')
router.register('approvereturnitem',ApproveReturnItemViewset,basename='approvereturnitem')
router.register('approval-issue',ApprovalIssueView,basename='approval-issue')
# router.register('approval-receipt',ApprovalReceiptView,basename='approval-receipt')

urlpatterns = [

    path('', include(router.urls)),
    path('transfer-item-list/<int:pk>/',TransferItemListView.as_view()),    
    path('transfer-item-list/',TransferItemListView.as_view()),
    path('received-item-list/<int:pk>/',ReceivedItemListView.as_view()),    
    path('received-item-list/',ReceivedItemListView.as_view()),
    path('return-item-list/<int:pk>/',ReturnItemListView.as_view()),    
    path('return-item-list/',ReturnItemListView.as_view()),
    path('transferstatus/<int:type>/',TransferStatusLiView.as_view()),
    path('tagged-item-number/<int:tag_number>/',TaggedItemListView.as_view()),
    path('tagged-branch-item-number/<int:tag_number>/<int:branch>/',TaggedBranchItemListView.as_view()),
    path('transfertype/',TransferTypeView.as_view()),
    path('transferfilterstatus/<int:type>/',TransferFilterStatusLiView.as_view()),
    
    # path('approval-transfer-list/<int:pk>/',ApprovalTransferListView.as_view()),   
    # path('approval-transfer-list/',ApprovalTransferListView.as_view()),
    path('approval-issue-details/<int:pk>/<int:gst_type>/', GetApprovalIssueDetails.as_view()),

    path('approval-issue-number/',ApprovalIssueNumberView.as_view()),
    path('approval-issue-list/',ApprovalIssueListView.as_view()),
    path('approval-recipt/<int:pk>/', ApprovalReciptView.as_view()),

    path('stock-ledger-type-list/', StockLedgerTypeList.as_view()),
    path('stock-ledger-list/', StockLedgerList.as_view()),
]