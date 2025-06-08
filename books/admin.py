from django.contrib import admin
from .models import *

# Register your models here.
class CompanyDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'company_name','is_active','mobile_no', 'email_id','created_at', 'created_by']  

    search_fields = ['company_name', 'mobile_no','email_id']
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(CompanyDetails,CompanyDetailsAdmin)

class CompanyAddressDetailsAdmin(admin.ModelAdmin):
    list_display = ['company_details', 'is_active' ,'door_no', 'street_name','area','taluk','created_at', 'created_by']  

    search_fields = ['company_name',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(CompanyAddressDetails,CompanyAddressDetailsAdmin)


class CompanyGstDetailsAdmin(admin.ModelAdmin):
    list_display = ['company_details', 'is_active',  'pan_no', 'gst_no','registered_name','gst_status','created_at', 'created_by']  

    search_fields = ['company_details','gst_no','pan_no','registered_name']
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(CompanyGstDetails,CompanyGstDetailsAdmin)

class CompanyBankDetailsAdmin(admin.ModelAdmin):
    list_display = ['company_details', 'is_active',  'acc_holder_name', 'account_no','ifsc_code','bank_name','created_at', 'created_by']  

    search_fields = ['company_details','acc_holder_name','account_no','ifsc_code']
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(CompanyBankDetails,CompanyBankDetailsAdmin)

class GroupLedgerAdmin(admin.ModelAdmin):
    list_display = ['group_ledger_name',]  

    search_fields = ['group_ledger_name',]
    
admin.site.register(GroupLedger,GroupLedgerAdmin)

class GroupTypeAdmin(admin.ModelAdmin):
    list_display = ['group_type_name',]  

    search_fields = ['group_type_name',]

admin.site.register(GroupType,GroupTypeAdmin)

class CustomerTypeAdmin(admin.ModelAdmin):
    list_display = ['customer_type_name',]  

    search_fields = ['customer_type_name',]

admin.site.register(CustomerType,CustomerTypeAdmin)

class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ['account_type_name',]  

    search_fields = ['account_type_name',]

admin.site.register(AccountType,AccountTypeAdmin)

class AccountHeadDetailsAdmin(admin.ModelAdmin):
    list_display = ['id','account_head_name', 'is_active',  'group_name','customer_type', 'account_type','created_at', 'created_by']  

    search_fields = ['account_head_name','group_name','customer_type' ,'account_type','account_type']
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(AccountHeadDetails,AccountHeadDetailsAdmin)

class AccountHeadAddressAdmin(admin.ModelAdmin):
    list_display = ['id','account_head', 'is_active',  'door_no','street_name', 'area','created_at', 'created_by']  

    search_fields = ['account_head','door_no','street_name' ,'area','taluk']
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(AccountHeadAddress,AccountHeadAddressAdmin)

class AccountHeadContactAdmin(admin.ModelAdmin):
    list_display = ['id','account_head', 'is_active',  'mobile_number','email_id', 'website','created_at', 'created_by']  

    search_fields = ['account_head','mobile_number','email_id' ,'website','landline_number']
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(AccountHeadContact,AccountHeadContactAdmin)

class AccountHeadBankDetailsAdmin(admin.ModelAdmin):
    list_display = ['id','account_head', 'is_active',  'acc_holder_name','account_no', 'bank_name','created_at', 'created_by']  

    search_fields = ['account_head','acc_holder_name','account_no' ,'ifsc_code','bank_name']
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(AccountHeadBankDetails,AccountHeadBankDetailsAdmin)

class AccountHeadGstDetailsAdmin(admin.ModelAdmin):
    list_display = ['id','account_head', 'is_active',  'pan_no','tin_no', 'gst_no','registered_name','created_at', 'created_by']  

    search_fields = ['account_head','pan_no','tin_no' ,'gst_no','registered_name']
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(AccountHeadGstDetails,AccountHeadGstDetailsAdmin)