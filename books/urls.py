from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('company',CompanyViewset,basename='company')
router.register('account-group',AccountGroupViewset,basename='account-group')
router.register('account-head',AccountHeadViewset,basename='account-head')

urlpatterns = [
    path('', include(router.urls)),

    path('company-list/',CompanyList.as_view()),
    path('company-list/<str:search>/',CompanyList.as_view()),
    path('company-bank-delete/<int:pk>/',CompanyBankView.as_view()),
    path('company-bank-delete/',CompanyBankView.as_view()),
    path('change-company-status/<int:pk>/',Companystatus.as_view()),

    path('group-ledger-list/',GroupLedgerView.as_view()),

    path('group-type-list/',GroupTypeView.as_view()),

    path('change-account-group-status/<int:pk>/',AccountGroupStatusView.as_view()),
    path('account-group-list/',AccountGroupListView.as_view()),

    path('customer-type-list/',CustomerTypeview.as_view()),

    path('account-type-list/',AccountTypeview.as_view()),

    path('account-head-list/',AccountHeadListView.as_view()),
    path('change-account-head-status/<int:pk>/',AccountHeadStatusView.as_view()),
    path('account-head-delete-address/',AccountHeadAddressView.as_view()),
    path('account-head-delete-contact/',AccountHeadContactView.as_view()),
    path('account-head-delete-bank/',AccountHeadBankView.as_view()),


]
