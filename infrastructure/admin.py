from django.contrib import admin
from .models import *

# Register your models here.
class CountereAdmin(admin.ModelAdmin):
    list_display = ['id','counter_name','floor','branch','is_active','created_at','created_by']  

    search_fields = ['counter_name',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(Counter,CountereAdmin)

class FloorAdmin(admin.ModelAdmin):
    list_display = ['id','floor_name','branch','is_active','created_at','created_by']  

    search_fields = ['floor_name',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(Floor,FloorAdmin)