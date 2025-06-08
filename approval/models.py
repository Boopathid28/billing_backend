from django.db import models
from accounts.models import *
# from settings.models import StatusType

class ApprovalType(models.Model):
    approval_type = models.CharField(verbose_name='Approval Type', max_length=100, unique=True)
    is_active = models.BooleanField(verbose_name='Active',default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", related_name="approval_type_created_by", on_delete=models.SET_DEFAULT, default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True, blank=True)
    modified_by = models.ForeignKey(User, verbose_name="Modified By", related_name="approval_type_modified_by", on_delete=models.SET_DEFAULT, default=1)

    class Meta:
        db_table="approval_types"
        verbose_name = 'approval_type'
        verbose_name_plural = 'approval_types'

    def __str__(self) -> str:
        return self.approval_type
    
class ApprovalRule(models.Model):
    approval_type = models.ForeignKey(ApprovalType, verbose_name='Approval Type', on_delete=models.PROTECT)
    user_role = models.ForeignKey(UserRole, verbose_name='User Role', on_delete=models.PROTECT)
    # branch = models.ForeignKey(Branch, verbose_name='Branch', on_delete=models.PROTECT,default=1)
    approved_by = models.ForeignKey(User, verbose_name="Created By", related_name="approved_by", on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(verbose_name="Created at", null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", related_name="approval_rule_created_by", on_delete=models.SET_DEFAULT, default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True, blank=True)
    modified_by = models.ForeignKey(User, verbose_name="Modified By", related_name="approval_rule_modified_by", on_delete=models.SET_DEFAULT, default=1)

    class Meta:
        db_table="approval_rules"
        verbose_name = 'approval_rule'
        verbose_name_plural = 'approval_rules'

    def __str__(self) -> str:
        return self.approval_type.approval_type
