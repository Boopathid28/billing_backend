from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register('trasfer-creation',TransferCreationView,basename='trasfer-creation')
router.register('melting-issue',MeltingIssueView,basename='melting-issue')
router.register('melting-recipt',MeltingReciptView,basename='melting-recipt')
router.register('purification-issue',PurificationIssueView,basename='purification-issue')
router.register('purification-recipt',PurificationReciptView,basename='purification-recipt')

urlpatterns = [ 
    path('', include(router.urls)),

    path('all-old-gold-list/', AllOldGoldList.as_view()),
    path('old-metal-category-list/', OldMetalCategoryListView.as_view()),
    path('transfer-creation-type-list/', TransferCreationTypeListView.as_view()),
    path('bag-number/', BagnumberView.as_view()),
    path('trasfer-creation-list/', TransferCreationList.as_view()),
    
    
    path('melting-issue-list/', MeltingIssueList.as_view()),
    path('melting-issue-number/', MeltingIssueNumberView.as_view()),
    
    
    path('melting-recipt-number/', MeltingReciptNumberView.as_view()),
    path('melting-recipt-list/', MeltingReciptListView.as_view()),
    
    
    path('purification-issue-number/', PurificationIssueNumberView.as_view()),
    path('purification-issue-list/', PurificationIssueListView.as_view()),
    
    
    path('purification-recipt-number/', PurificationReciptNumberView.as_view()),
    path('purification-recipt-list/', PurificationReciptListView.as_view()),
    
]