from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register('floor', FloorViewSet, basename='floor')
router.register('counter', CounterViewSet, basename='counter')
router.register('counter-target', CounterTargetView, basename='counter-target')

urlpatterns = [
    # router urls included
    path('', include(router.urls)),
    

    # Floor APIs
    path('floor-list/', FloorList.as_view()),
    path('floor-list/<int:branch>/', FloorList.as_view()),
    path('change-floor-status/<int:pk>/', FloorStatus.as_view()),

    # Counter APIs
    path('counter-list/', CounterList.as_view()),
    path('counter-list/<int:branch>', CounterList.as_view()),
    path('change-counter-status/<int:pk>/', CounterStatus.as_view()),

    #Counter Target List
    path('counter-target-list/',CounterTargetListView.as_view())
]