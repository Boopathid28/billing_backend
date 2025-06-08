from django.contrib import admin
from .models import *

# Register your models here.


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id','department_name','is_active','created_at','created_by']  

    search_fields = ['department_name',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(Department,DepartmentAdmin)

class DesignationAdmin(admin.ModelAdmin):
    list_display = ['id','designation_name','is_active','created_at','created_by']  

    search_fields = ['designation_name',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(Designation,DesignationAdmin)
