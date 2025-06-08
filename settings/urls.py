from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register('user-role', UserRoleViewSet, basename='user-role')
router.register('menu-group', MenuGroupViewSet, basename='menu-group')
router.register('menu', MenuViewSet, basename='menu')
router.register('main-menu', MainMenuGroupViewSet, basename='main-menu')
router.register('incentive-type', IncentiveTypeViewSet, basename='incentive-type')
router.register('incentive-percent', IncentivePercentViewSet, basename='incentive-percent')

urlpatterns = [
    # router urls included
    path('', include(router.urls)),
    # User Role APIs
    path('user-role-list/', UserRolesList.as_view()),
    path('change-user-role-status/<int:pk>/', UserRolesStatus.as_view()),
    path('change-user-role-admin-status/<int:pk>/', UserRoleAdminStatus.as_view()),

    # Menu Group APIs
    path('menu-group-list/', MenuGroupList.as_view()),
    path('menu-group-list/<int:main_menu>/', MenuGroupList.as_view()),
    path('change-menu-group-status/<int:pk>/', MenuGroupStatus.as_view()),

    # Menu Group APIs
    path('menu-list/', MenuList.as_view()),
    path('menu-list/<int:menu_group>/', MenuList.as_view()),
    path('change-menu-status/<int:pk>/', MenuStatus.as_view()),

    # Menu Permission APIs
    path('menu-permission/', MenuPermissionView.as_view()),
    path('menu-permission/<int:pk>/', MenuPermissionView.as_view()),
    path('active-user-menu-permission/', ActiveUserMenuPermissionView.as_view()),

    # Verification APIs
    path('gst-verification/<str:gst>/',GstVerificationView.as_view()),
    path('ifsc-verification/<str:ifsc>/',IFSCVerificationView.as_view()),

    #status APIs
    path('status-list/<int:pk>/',StatusLiView.as_view()),

    #payment_mode APIs
    path('payment-mode/<int:pk>/',PaymentModeView.as_view()),

    #gender APIs
    path('gender-list/', GendersList.as_view()),
    
    #payment_mode APIs
    path('payment-status/',PaymentStatusView.as_view()),

    #Return Policy
    path('return-policy/',SaleReturnPolicyView.as_view()),

    #secret_key
    path('verification/',AdminSecret.as_view()),

    path('print-list/',PrintList.as_view()),
    path('print-status-change/<int:pk>/',PrintStatusChange.as_view()),
    
    path('data-injection/',DataInjectionView.as_view()),

    #MAIN MENU GROUP STATUS
    path('main-menu-list/', MainMenuGroupList.as_view()),
    path('change-main-menu-status/<int:pk>/', MainMenuGroupStatus.as_view()),

    path('incentive-list/', IncentiveList.as_view()),

    path('sales-entry-type/', SalesEntryTypeView.as_view()),
    path('transaction-type/', TransactionTypeView.as_view()),

]