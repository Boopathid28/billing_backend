from django.contrib import admin
from .models import *

class MenuGroupAdmin(admin.ModelAdmin):
    list_display = ['menu_group_name', 'main_menu_group','icon', 'is_active', 'created_at', 'created_by']

    list_editable=['main_menu_group', 'is_active']

    readonly_fields = ['modified_by', 'modified_at', 'created_at',]

admin.site.register(MenuGroup, MenuGroupAdmin)

class MenuAdmin(admin.ModelAdmin):
    list_display = ['menu_name', 'menu_group','menu_path', 'icon', 'is_active', 'created_at', 'created_by']

    list_editable=[ 'menu_group','menu_path',  'is_active', ]

    readonly_fields = ['modified_by', 'modified_at', 'created_at', 'menu_path']

admin.site.register(Menu, MenuAdmin)

class MenuPermissionAdmin(admin.ModelAdmin):
    list_display = ['menu', 'user_role', 'view_permit', 'add_permit', 'edit_permit', 'delete_permit', 'created_by']

    list_editable=['view_permit', 'add_permit', 'edit_permit', 'delete_permit']

    readonly_fields = ['modified_at', ]

admin.site.register(MenuPermission, MenuPermissionAdmin)

class GenderAdmin(admin.ModelAdmin):

    list_display = ['name', 'is_active', 'created_at', 'created_by']

admin.site.register(Gender, GenderAdmin)


@admin.register(StatusTable)
class StatusTableAdmin(admin.ModelAdmin):

    list_display = ('id', 'status_name','module')

@admin.register(PrintModule)
class PrintModuleAdmin(admin.ModelAdmin):

    list_display = ('id', 'estimation_is_a4','billing_is_a4','order_is_a4','repair_is_a4')

class MainMenuGroupAdmin(admin.ModelAdmin):
    
    list_display = ['main_menugroup_name', 'is_active', 'created_at', 'created_by']

    readonly_fields = ['modified_by', 'modified_at', 'created_at',]

admin.site.register(MainMenuGroup, MainMenuGroupAdmin)

class IncentiveTypeAdmin(admin.ModelAdmin):
    
    list_display = ['incentive_typename', 'is_active', 'created_at', 'created_by']

    readonly_fields = ['modified_by', 'modified_at', 'created_at',]

admin.site.register(IncentiveType, IncentiveTypeAdmin)


class IncentivePercentAdmin(admin.ModelAdmin):
    
    list_display = ['incentive_type', 'is_active', 'created_at', 'created_by','incentive_percent','from_amount','to_amount']

    readonly_fields = ['modified_by', 'modified_at', 'created_at',]

admin.site.register(IncentivePercent, IncentivePercentAdmin)


class SalesEntryTypeAdmin(admin.ModelAdmin):
    
    list_display = ['entry_type_name', 'is_active', 'created_at', 'created_by',]

    readonly_fields = ['created_at',]

admin.site.register(SalesEntryType, SalesEntryTypeAdmin)


class TransactionTypeAdmin(admin.ModelAdmin):
    
    list_display = ['transaction_type', 'is_active', 'created_at', 'created_by',]

    readonly_fields = ['created_at','created_by',]

admin.site.register(TransactionType, TransactionTypeAdmin)