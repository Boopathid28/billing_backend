from django.contrib import admin
from .models import *

# Register your models here.

class AdvancePurposeAdmin(admin.ModelAdmin):
    list_display = ['purpose_name','is_active','created_at','created_by']  

    search_fields = ['purpose_name',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(AdvancePurpose,AdvancePurposeAdmin)

class AdvanceDetailsAdmin(admin.ModelAdmin):
    list_display = ['customer_details','advance_id','total_advance_amount','advance_weight_purity','total_advance_weight','advance_purpose','created_at','created_by']  

    search_fields = ['customer_details','advance_id',]
    
    readonly_fields = ['created_at',]

    list_editable=[]

admin.site.register(AdvanceDetails,AdvanceDetailsAdmin)