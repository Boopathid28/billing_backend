from django.contrib import admin
from .models import *
# Register your models here.
class RepairDetailsAdmin(admin.ModelAdmin):
    list_display = ['repair_number','repair_for','customer_details','created_at','created_by']  

    search_fields = ['repair_number']
    
    readonly_fields = ['modified_at',]

    list_editable=['repair_for',]

admin.site.register(RepairDetails,RepairDetailsAdmin)

class RepairItemDetailsAdmin(admin.ModelAdmin):
    list_display = ['repair_order_details','repair_type','item_details','created_at','created_by']  

    search_fields = ['repair_order_details']
    
    readonly_fields = ['modified_at',]

    list_editable=['repair_type',]

admin.site.register(RepairItemDetails,RepairItemDetailsAdmin)


class RepairOrderIssuedAdmin(admin.ModelAdmin):
    list_display = ['repair_details','vendor_name','issue_date','payment_status','created_at','created_by']  

    search_fields = ['repair_details']
    
    readonly_fields = ['modified_at',]

    list_editable=['payment_status',]

admin.site.register(RepairOrderIssued,RepairOrderIssuedAdmin)

class RepairOrderNumberAdmin(admin.ModelAdmin):
    list_display = ['created_at','created_by']  

    search_fields = ['created_by']
    
    readonly_fields = ['modified_at']

    list_editable=['created_by']

admin.site.register(RepairOrderNumber,RepairOrderNumberAdmin)

class RepairForAdmin(admin.ModelAdmin):
    list_display = ['repair_for','created_at','created_by']  

    search_fields = ['repair_for','created_by']
    
    readonly_fields = ['modified_at']

    list_editable=['created_by']

admin.site.register(RepairFor,RepairForAdmin)