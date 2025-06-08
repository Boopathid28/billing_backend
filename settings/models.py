from django.db import models
from accounts.models import *
from settings.models import *

class MainMenuGroup(models.Model):

    main_menugroup_name = models.CharField(max_length=50, verbose_name='Main Menu group name', unique=True)
    is_active = models.BooleanField(default=True, verbose_name='Status')
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING)
    modified_by = models.IntegerField(verbose_name='Modified by', null=True, blank=True)

    class Meta:
        db_table = 'main_menu_group'
        verbose_name = 'main_menu_group'
        verbose_name_plural = 'main_menu_groups'

    def __str__(self) -> str:
        return self.main_menugroup_name

class MenuGroup(models.Model):

    menu_group_name = models.CharField(max_length=50, verbose_name='Menu group name', unique=True)
    main_menu_group = models.ForeignKey(MainMenuGroup, verbose_name='Main Menu Group', on_delete=models.PROTECT,null=True)
    icon = models.FileField(verbose_name='Icon', upload_to="menugroup_icon/", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Status')
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING)
    modified_by = models.IntegerField(verbose_name='Modified by', null=True, blank=True)

    class Meta:
        db_table = 'menu_groups'
        verbose_name = 'menu_group'
        verbose_name_plural = 'menu_groups'

    def __str__(self) -> str:
        return self.menu_group_name

class Menu(models.Model):

    menu_name = models.CharField(max_length=50, verbose_name='Menu name', unique=True)
    menu_path = models.CharField(max_length=50, verbose_name='Menu path', unique=True)
    menu_group = models.ForeignKey(MenuGroup, verbose_name='Menu Group', on_delete=models.PROTECT)
    icon = models.FileField(verbose_name='Icon', upload_to="menu_icon/",null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Status')
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING)
    modified_by = models.IntegerField(verbose_name='Modified by', null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.menu_path = "/" + "/".join(["-".join(self.menu_group.menu_group_name.split(' ')), "-".join(self.menu_name.split(' '))])
    #     super().save(update_fields=['menu_path'])

    class Meta:
        db_table = 'menus'
        verbose_name = 'menu'
        verbose_name_plural = 'menus'

    def __str__(self) -> str:
        return self.menu_name
    

class MenuPermission(models.Model):

    menu = models.ForeignKey(Menu, verbose_name='Menu', on_delete=models.CASCADE)
    user_role = models.ForeignKey(UserRole, verbose_name='User role', on_delete=models.CASCADE)
    view_permit = models.BooleanField(default=True, verbose_name='View')
    add_permit = models.BooleanField(default=False, verbose_name='Add')
    edit_permit = models.BooleanField(default=False, verbose_name='Edit')
    delete_permit = models.BooleanField(default=False, verbose_name='Delete')
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'menu_permissions'
        verbose_name = 'menu_permission'
        verbose_name_plural = 'menu_permissions'

    def __str__(self) -> str:
        return self.menu.menu_name
    
class StatusTable(models.Model):
    status_name=models.CharField(max_length=50,verbose_name="Status Name")
    module=models.CharField(max_length=50,verbose_name="Module")
    color = models.CharField(max_length=20,verbose_name="lot color",null=True,blank=True)
    class Meta:
        db_table = 'status_table'
        verbose_name = 'status_table'
        verbose_name_plural = 'status_tables'

    def __str__(self) -> str:
        return self.status_name

class PaymentMode(models.Model):
    mode_name=models.CharField(max_length=50,verbose_name="Mode Name")
    short_code=models.CharField(max_length=50,verbose_name="Payment Short Code ")
    color = models.CharField(max_length=20,verbose_name="Payment Mode color",null=True,blank=True)
    class Meta:
        db_table = 'payment_mode'
        verbose_name = 'payment_mode'
        verbose_name_plural = 'payment_mode'

    def __str__(self) -> str:
        return self.mode_name

class PaymentStatus(models.Model):
    status_name=models.CharField(max_length=50,verbose_name="Status Name")
    color = models.CharField(max_length=20,verbose_name="Payment Status color",null=True,blank=True)
    class Meta:
        db_table = 'payment_status'
        verbose_name = 'payment_status'
        verbose_name_plural = 'payment_status'

    def __str__(self) -> str:
        return self.status_name
    
    
class SaleReturnPolicy(models.Model):
    return_days=models.IntegerField(verbose_name="Return Days")
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING,related_name="return_policy_created_by",null=True, blank=True)
    modified_by = models.ForeignKey(User,verbose_name='Modified by', on_delete=models.DO_NOTHING,related_name="return_policy_modified_by", null=True, blank=True)
    class Meta:
        db_table = 'sale_return_policy'
        verbose_name = 'sale_return_policy'
        verbose_name_plural = 'sale_return_policy'

    def __str__(self) -> str:
        return self.return_days

class Gender(models.Model):

    name = models.CharField(verbose_name="Gendor Name", max_length=100)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', related_name='gender_created_by', on_delete=models.DO_NOTHING,null=True,blank=True)

    class Meta:
        db_table = 'settings_gender'
        verbose_name = 'settings_gender'
        verbose_name_plural = 'settings_genders'

class PrintModule(models.Model):

    estimation_is_a4=models.BooleanField(verbose_name="Estimation Is A4",default=True)
    billing_is_a4=models.BooleanField(verbose_name="Billing Is A4",default=True)
    billing_backup_is_a4=models.BooleanField(verbose_name="Billing Backup Is A4",default=True)
    order_is_a4=models.BooleanField(verbose_name="Order Is A4",default=True)
    repair_is_a4=models.BooleanField(verbose_name="Repair Is A4",default=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', related_name='print_created_by', on_delete=models.DO_NOTHING,null=True,blank=True)

    class Meta:
        db_table = 'print_module'
        verbose_name = 'print_module'
        verbose_name_plural = 'print_modules'


class IncentiveType(models.Model):
    incentive_typename=models.CharField(max_length=10,verbose_name="Incentive type name")
    is_active=models.BooleanField(verbose_name="Active status",default=True)   
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', related_name='incentive_typename_created_by', on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    modified_by = models.ForeignKey(User, verbose_name='Modified by', related_name='incentive_typename_modified_by', on_delete=models.DO_NOTHING,null=True, blank=True)

    class Meta:
        db_table = 'incentive_type'
        verbose_name = 'incentive_types'
        verbose_name_plural = 'incentive_types'

class IncentivePercent(models.Model):
    incentive_type=models.ForeignKey(IncentiveType,related_name="incentive_type",on_delete=models.DO_NOTHING)
    incentive_percent = models.FloatField(verbose_name='Incentive percentage',null=True, blank=True)
    incentive_amount = models.FloatField(verbose_name='Incentive amount',null=True, blank=True)
    from_amount = models.FloatField(verbose_name='Incentive from amount')
    to_amount = models.FloatField(verbose_name='Incentive to amount')
    is_active=models.BooleanField(verbose_name="Active status",default=True)   
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', related_name='incentive_created_by', on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    modified_by = models.ForeignKey(User, verbose_name='Modified by', related_name='incentive_modified_by', on_delete=models.DO_NOTHING,null=True, blank=True)

    class Meta:
        db_table = 'incentive_percent'
        verbose_name = 'incentive_percents'
        verbose_name_plural = 'incentive_percents'


class SalesEntryType(models.Model):

    entry_type_name=models.CharField(max_length=100,verbose_name="Entry Type",unique=True)
    is_active = models.BooleanField(verbose_name="Active Status",default=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING,null=True,blank=True)

    class Meta:
        db_table = 'sale_entry_type'
        verbose_name = 'sale_entry_type'
        verbose_name_plural = 'sales_entry_type'


class TransactionType(models.Model):

    transaction_type=models.CharField(max_length=100,verbose_name="Transaction Type",unique=True)
    is_active = models.BooleanField(verbose_name="Active Status",default=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING,null=True,blank=True)

    class Meta:
        db_table = 'transaction_type'
        verbose_name = 'transaction_type'
        verbose_name_plural = 'transaction_types'