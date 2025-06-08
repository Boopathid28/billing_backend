from django.contrib import admin
from approval.models import ApprovalType,ApprovalRule

class ApprovalTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'approval_type','is_active','created_at', 'created_by']  

    search_fields = ['approval_type']
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(ApprovalType,ApprovalTypeAdmin)

class ApprovalRuleAdmin(admin.ModelAdmin):
    list_display = ['id','approval_type','user_role','approved_by','is_active','created_at', 'created_by']  

    search_fields = ['approval_type','user_role','approved_by']
    
    readonly_fields = ['modified_at',]

    list_editable=['is_active',]

admin.site.register(ApprovalRule,ApprovalRuleAdmin)