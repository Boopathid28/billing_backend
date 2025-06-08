from django.contrib import admin
from .models import *

# Register your models here.
class RangeStockAdmin(admin.ModelAdmin):
    list_display = ['from_weight','to_weight','range_value','is_active','created_at']  

    search_fields = ['from_weight','to_weight','range_value']
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(RangeStock,RangeStockAdmin)

class CalculationTypeAdmin(admin.ModelAdmin):
    list_display = ['id','calculation_name','is_active','created_at','created_by']  

    search_fields = ['calculation_name',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(CalculationType,CalculationTypeAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ['id','item_id','item_name','metal','is_active','created_at','created_by']  

    search_fields = ['item_name',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(Item,ItemAdmin)


class FixedRateAdmin(admin.ModelAdmin):
    list_display = ['item_details','fixed_rate','created_at','created_by']  

    search_fields = ['item_details',]
    
    readonly_fields = ['modified_at',]

admin.site.register(FixedRate,FixedRateAdmin)

class WeightCalculationAdmin(admin.ModelAdmin):
    list_display = ['item_details','wastage_calculation','created_at','created_by']  

    search_fields = ['item_details',]
    
    readonly_fields = ['modified_at',]

admin.site.register(WeightCalculation,WeightCalculationAdmin)

class WeightTypeAdmin(admin.ModelAdmin):
    list_display = ['id','weight_name','is_active','created_at','created_by']  

    search_fields = ['weight_name',]
    
    readonly_fields = ['modified_at',]

admin.site.register(WeightType,WeightTypeAdmin)

class StockTypeAdmin(admin.ModelAdmin):
    list_display = ['stock_type_name','is_active','created_at','created_by']  

    search_fields = ['stock_type_name',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(StockType,StockTypeAdmin)


class SubItemAdmin(admin.ModelAdmin):
    list_display = ['id','sub_item_id','sub_item_name','metal','is_active','created_at','created_by']  

    search_fields = ['sub_item_name',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(SubItem,SubItemAdmin)


class SubItemFixedRateAdmin(admin.ModelAdmin):
    list_display = ['sub_item_details','fixed_rate','created_at','created_by']  

    search_fields = ['sub_item_details',]
    
    readonly_fields = ['modified_at',]

admin.site.register(SubItemFixedRate,SubItemFixedRateAdmin)

class SubItemWeightCalculationAdmin(admin.ModelAdmin):
    list_display = ['sub_item_details','wastage_calculation','created_at','created_by']  

    search_fields = ['item_details',]
    
    readonly_fields = ['modified_at',]

admin.site.register(SubItemWeightCalculation,SubItemWeightCalculationAdmin)


class MeasurementTypeAdmin(admin.ModelAdmin):
    list_display = ['measurement_name','created_at','created_by']  

    search_fields = ['measurement_name',]
    
    readonly_fields = ['modified_at',]

admin.site.register(MeasurementType,MeasurementTypeAdmin)
