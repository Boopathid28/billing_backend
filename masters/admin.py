from django.contrib import admin
from .models import *

# Register your models here.

class MetalAdmin(admin.ModelAdmin):
    list_display = ['id','metal_name','metal_code','is_active']  

    search_fields = ['metal_name','metal_code']
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(Metal,MetalAdmin)

class PurityAdmin(admin.ModelAdmin):
    list_display = ['purity_name','purity_code','purrity_percent','metal','is_active']  

    search_fields = ['purity_name','purity_code','metal']
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(Purity,PurityAdmin)


class TaxDetailsAdmin(admin.ModelAdmin):
    list_display = ['metal','tax_code','tax_name','tax_description','is_active']  

    search_fields = ['metal','tax_code','tax_name','tax_description']
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(TaxDetails,TaxDetailsAdmin)

class PurchaseTaxDetailsAdmin(admin.ModelAdmin):
    list_display = ['tax_details','purchase_tax_igst','purchase_tax_cgst','purchase_tax_sgst','purchase_surcharge_percent','purchase_additional_charges']  

    search_fields = ['tax_details','purchase_tax_igst','purchase_tax_cgst','purchase_tax_sgst','purchase_surcharge_percent','purchase_additional_charges']
    
    readonly_fields = ['modified_at',]

admin.site.register(PurchaseTaxDetails,PurchaseTaxDetailsAdmin)

class SalesTaxDetailsAdmin(admin.ModelAdmin):
    list_display = ['tax_details','sales_tax_igst','sales_tax_cgst','sales_tax_sgst','sales_surcharge_percent','sales_additional_charges']  

    search_fields = ['tax_details','sales_tax_igst','sales_tax_cgst','sales_tax_sgst','sales_surcharge_percent','sales_additional_charges']
    
    readonly_fields = ['modified_at',]

admin.site.register(SalesTaxDetails,SalesTaxDetailsAdmin)

class ShapeDetailsAdmin(admin.ModelAdmin):
    list_display = ['shape_name','is_active','created_at']  

    search_fields = ['shape_name',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(ShapeDetails,ShapeDetailsAdmin)

class CutDetailsAdmin(admin.ModelAdmin):
    list_display = ['cut_name','is_active','created_at']  

    search_fields = ['cut_name',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(CutDetails,CutDetailsAdmin)

class ColorDetailsAdmin(admin.ModelAdmin):
    list_display = ['color_name','is_active','created_at']  

    search_fields = ['color_name',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(ColorDetails,ColorDetailsAdmin)

class ClarityDetailsAdmin(admin.ModelAdmin):
    list_display = ['clarity_name','is_active','created_at']  

    search_fields = ['clarity_name',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(ClarityDetails,ClarityDetailsAdmin)

class CentGroupAdmin(admin.ModelAdmin):
    list_display = ['centgroup_name','is_active','created_at']  

    search_fields = ['centgroup_name',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(CentGroup,CentGroupAdmin)

class StoneAdmin(admin.ModelAdmin):
    list_display = ['stone_name','stone_code','reduce_weight','is_active','created_at']  

    search_fields = ['stone_name','stone_code',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(StoneDetails,StoneAdmin)

class CaratRateAdmin(admin.ModelAdmin):
    list_display = ['designer','stone','shape','cut','color','clarity','cent_group','purchase_rate','selling_rate','is_active','created_at']  

    search_fields = ['designer','stone','shape','cut','color','clarity','cent_group']
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(CaratRate,CaratRateAdmin)



class TaxDetailsAuditAdmin(admin.ModelAdmin):
    list_display = ['metal','tax_details','created_at']  

    search_fields = ['metal','tax_details']
    
    readonly_fields = ['modified_at',]

    list_editable=['tax_details',]

admin.site.register(TaxDetailsAudit,TaxDetailsAuditAdmin)

class MetalOldRateAdmin(admin.ModelAdmin):
    list_display = ['metal','old_metal_rate','created_at']  

    search_fields = ['metal','old_metal_rate']
    
    readonly_fields = ['modified_at',]

    list_editable=['old_metal_rate',]

admin.site.register(MetalOldRate,MetalOldRateAdmin)

class VoucherTypeAdmin(admin.ModelAdmin):
    list_display = ['voucher_name','is_active','created_at']  

    search_fields = ['voucher_name','is_active']
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(VoucherType,VoucherTypeAdmin)

class GiftVoucherAdmin(admin.ModelAdmin):
    list_display = ['voucher_type','voucher_no','cash','is_active','is_redeemed','created_at']  

    search_fields = ['voucher_type','voucher_no','is_active']
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(GiftVoucher,GiftVoucherAdmin)

class RepairTypeAdmin(admin.ModelAdmin):
    list_display = ['repair_type_name','is_active','created_at']  

    search_fields = ['repair_type_name','is_active']
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(RepairType,RepairTypeAdmin)

class GSTTypeAdmin(admin.ModelAdmin):
    list_display = ['gst_type_name','is_active','created_at']  

    search_fields = ['gst_type_name','is_active']
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(GSTType,GSTTypeAdmin)