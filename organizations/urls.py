from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register('location', LocationViewSet, basename='location')
router.register('branch', BranchViewSet, basename='branch')
router.register('department', DepartmentViewSet, basename='department')
router.register('designation', DesignationViewSet, basename='designation')
router.register('staff', StaffViewSet, basename='staff')
router.register('user', UserViewSet, basename='user')

urlpatterns = [
    # router urls included
    path('', include(router.urls)),

    # Location APIs
    path('location-list/', LocationList.as_view()),
    path('change-location-status/<int:pk>/', LocationStatus.as_view()),

    # Branch APIs
    path('branch-list/', BranchList.as_view()),
    path('branch-list/<str:location>/', BranchList.as_view()),
    path('change-branch-status/<int:pk>/', BranchStatus.as_view()),

    # Department APIs
    path('department-list/', DepartmentList.as_view()),
    path('change-department-status/<int:pk>/', DepartmentStatus.as_view()),

    # Designation APIs
    path('designation-list/', DesignationList.as_view()),
    path('change-designation-status/<int:pk>/', DesignationStatus.as_view()),

    # Staff APIs
    path('staff-list/', StaffList.as_view()),
    path('staff-branch-list/', StaffBranchList.as_view()),
    path('staff-branch-list/<int:branch>/', StaffBranchList.as_view()),
    path('change-staff-status/<int:pk>/', StaffStatus.as_view()),

    # User APIs
    path('user-list/', UserList.as_view()),
    path('change-user-status/<int:pk>/', UserStatus.as_view()),
    path('user-list-by-userrole/<int:pk>/', UserListByUserRole.as_view()),
    
]