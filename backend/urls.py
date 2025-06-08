"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path
from django.conf import settings
from django.conf.urls.static import static, serve
urlpatterns = [
    path('admin/', admin.site.urls),
    path('settings/', include('settings.urls')),
    path('accounts/', include('accounts.urls')),
    path('organizations/', include('organizations.urls')),
    path('infrastructure/', include('infrastructure.urls')),
    path('masters/', include('masters.urls')),
    path('books/', include('books.urls')),
    path('product/', include('product.urls')),
    path('tagging/', include('tagging.urls')),
    path('billing/', include('billing.urls')),
    path('value-addition/', include('value_addition.urls')),
    path('customer/', include('customer.urls')),
    path('advance-payment/', include('advance_payment.urls')),
    path('order/', include('order_management.urls')),
    path('approval/', include('approval.urls')),
    path('stock/', include('stock.urls')),
    path('report/', include('reports.urls')),
    path('purchase/', include('purchase.urls')),
    path('billing_backup/', include('billing_backup.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('repair-management/', include('repair_management.urls')),
    path('refinery-management/', include('refinery_management.urls')),
    path('payment-management/', include('payment_management.urls')),
    path('financial-accounting/', include('financial_accounting.urls')),
    path('oldgold-management/', include('old_gold_management.urls')),
    path('suspense-management/', include('suspense_management.urls')),
    path('vendor-management/', include('vendor_management.urls')),
    path('old-gold-ledger/', include('old_gold_ledger.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    

]
