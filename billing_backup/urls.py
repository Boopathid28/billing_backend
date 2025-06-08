from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),

    path('backup-bill-gold-number/', BackupGoldBillnumberView.as_view()),
    path('backup-bill-silver-number/', BackupSilverBillnumberView.as_view()),
    path('sale-bill-backup/',BillinBackupView.as_view()),
    path('sale-bill-backup/<int:pk>/',BillinBackupView.as_view()),
    path('truncate-model/',TruncateModelView.as_view()),
    path('delete-model/',DeleteModelView.as_view()),

]

    
