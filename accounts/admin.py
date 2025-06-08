from django.contrib import admin
from .models import *
from rest_framework.authtoken.models import Token
from django.contrib.sessions.models import Session

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


class BranchAdmin(admin.ModelAdmin):
    list_display = ['id','branch_name','location','is_active','created_at']  

    search_fields = ['branch_name',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]


class LocationAdmin(admin.ModelAdmin):
    list_display = ['id','location_name','is_active','created_at']  

    search_fields = ['location_name',]
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['role_name', 'is_active', 'created_at']

    search_fields = ['role_name']
    
    readonly_fields = ['modified_at',]

class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone','is_active', 'created_at']

    search_fields = ['email', 'phone']

    readonly_fields = ['modified_at', 'modified_by', 'deleted_at', 'deleted_by']

admin.site.register(Branch,BranchAdmin)
admin.site.register(Location,LocationAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Token)
admin.site.register(Session, SessionAdmin)
