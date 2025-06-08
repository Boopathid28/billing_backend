from django.contrib import admin
from .models import *

# Register your models here.
class OrderForAdmin(admin.ModelAdmin):
    list_display = ['name','is_active','created_at']  

    search_fields = ['name']
    
    list_editable=['is_active',]

admin.site.register(OrderFor, OrderForAdmin)

class PriorityAdmin(admin.ModelAdmin):
    list_display = ['name','is_active','created_at']  

    search_fields = ['name']
    
    list_editable=['is_active',]

admin.site.register(Priority, PriorityAdmin)

class OrderItemAttachmentsAdmin(admin.ModelAdmin):

    list_display = ['image']

admin.site.register(OrderItemAttachments, OrderItemAttachmentsAdmin)

class OrderIdAdmin(admin.ModelAdmin):

    list_display = ['order_id', 'created_at', 'created_by']

admin.site.register(OrderId, OrderIdAdmin)

class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'approximate_amount' ]  

    search_fields = ['order_id']

admin.site.register(OrderDetails, OrderDetailsAdmin)

class OrderItemDetailsAdmin(admin.ModelAdmin):
    list_display = ['gross_weight', 'net_weight', 'metal_rate', 'actual_amount', 'total_amount', 'is_recieved']  

    search_fields = []

    list_editable = ['is_recieved']

admin.site.register(OrderItemDetails, OrderItemDetailsAdmin)
