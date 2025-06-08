from django.contrib import admin
from .models import *

# Register your models here.

class CustomerGroupAdmin(admin.ModelAdmin):
    list_display = ['customer_group_name','is_active','created_at','created_by']  

    search_fields = ['customer_group_name',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(CustomerGroup,CustomerGroupAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','customer_name','customer_group','is_active','created_at','created_by']  

    search_fields = ['customer_name',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(Customer,CustomerAdmin)
