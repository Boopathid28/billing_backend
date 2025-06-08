from django.db import models
from accounts.models import *
from customer.models import Customer
from masters.models import Metal, Purity, StoneDetails, GSTType
from product.models import Item, SubItem, MeasurementType, CalculationType, WeightType
from tagging.models import StoneWeightType, RateType
from settings.models import StatusTable, Gender, PaymentStatus
from django.conf import settings
from books.models import AccountHeadDetails

class OrderFor(models.Model):

    name = models.CharField(verbose_name="Order For Name", max_length=100)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', related_name='order_for_created_by', on_delete=models.DO_NOTHING,null=True,blank=True)

    class Meta:
        db_table = 'order_management_order_for'
        verbose_name = 'order_management_order_for'
        verbose_name_plural = 'order_management_order_fors'

    def __str__(self) -> str:
        return self.name
    
class Priority(models.Model):

    name = models.CharField(verbose_name="Priority Name", max_length=100)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', related_name='priority_created_by', on_delete=models.DO_NOTHING,null=True,blank=True)

    class Meta:
        db_table = 'order_management_priority'
        verbose_name = 'order_management_priority'
        verbose_name_plural = 'order_management_priorities'

    def __str__(self) -> str:
        return self.name
    

class OrderId(models.Model):

    order_id = models.CharField(verbose_name="Order Id", max_length=100, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', related_name='order_id_created_by', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'order_management_order_id'
        verbose_name = 'order_management_order_id'
        verbose_name_plural = 'order_management_order_ids'

    def __str__(self) -> str:
        return self.order_id
    
class SessionOrderId(models.Model):

    ses_order_id = models.OneToOneField(OrderId, verbose_name='Order Id', on_delete=models.CASCADE)
    user = models.OneToOneField(User, verbose_name='User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'order_management_session_order_id'
        verbose_name = 'order_management_session_order_id'
        verbose_name_plural = 'order_management_session_order_ids'

    def __str__(self) -> str:
        return self.ses_order_id
    
class OrderDetails(models.Model):

    order_id = models.OneToOneField(OrderId, verbose_name='Order Id', on_delete=models.CASCADE)
    order_for = models.ForeignKey(OrderFor, verbose_name='Order For', on_delete=models.PROTECT)
    priority = models.ForeignKey(Priority, verbose_name='Priority', on_delete=models.PROTECT)
    order_date = models.DateField(verbose_name='Order Date')
    no_of_days = models.IntegerField(verbose_name='No of Days')
    due_date = models.DateField(verbose_name='Due Date')
    branch = models.ForeignKey(Branch, verbose_name='Branch', on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, verbose_name='Customer', on_delete=models.PROTECT, null=True, blank=True)
    customer_name = models.CharField(max_length=50, verbose_name="Customer Name",null=True, blank=True)
    total_weight = models.FloatField(verbose_name='Total Weight')
    total_quantity = models.IntegerField(verbose_name='Total Quantity')
    approximate_amount = models.FloatField(verbose_name='Approximate Amount')
    is_order_scheduled = models.BooleanField(default=False, verbose_name='Order scheduled')
    order_status = models.ForeignKey(StatusTable, verbose_name='Order Status', related_name="order_details_order_status", on_delete=models.PROTECT, default=settings.PENDING)
    payment_status = models.ForeignKey(PaymentStatus, verbose_name='Payment Status', related_name="order_details_payment_status", on_delete=models.PROTECT, default=settings.PENDING)
    is_issued=models.BooleanField(verbose_name="Is issued",default=False)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', related_name='order_details_created_by', on_delete=models.DO_NOTHING)
    modified_by = models.ForeignKey(User, verbose_name='Modified by', related_name='order_details_modified_by', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'order_management_order_detail'
        verbose_name = 'order_management_order_detail'
        verbose_name_plural = 'order_management_order_details'

    def __str__(self) -> str:
        return self.order_id.order_id
    
class OrderItemDetails(models.Model):

    order_id = models.ForeignKey(OrderId, verbose_name='Order Id', on_delete=models.CASCADE)
    metal = models.ForeignKey(Metal, verbose_name='Metal', on_delete=models.PROTECT)
    purity = models.ForeignKey(Purity, verbose_name='Purity', on_delete=models.PROTECT)
    item = models.ForeignKey(Item, verbose_name='Item', on_delete=models.PROTECT)
    sub_item = models.ForeignKey(SubItem, verbose_name='Sub Item', on_delete=models.PROTECT)
    gross_weight = models.FloatField(verbose_name='Gross Weight')
    net_weight = models.FloatField(verbose_name='Net Weight')
    metal_rate = models.FloatField(verbose_name="Metal Rate")
    pieces = models.IntegerField(verbose_name='pieces',default=0 )
    gender = models.ForeignKey(Gender, verbose_name='Gender Type', on_delete=models.PROTECT)
    measurement_type = models.ForeignKey(MeasurementType, verbose_name='Measurement Type', on_delete=models.PROTECT, null=True, blank=True)
    measurement_value = models.CharField(max_length=50,verbose_name='Measurement Value', null=True, blank=True)
    total_stone_weight = models.FloatField(verbose_name='Total Stone Weight', default=0.0)
    total_stone_pieces = models.IntegerField(verbose_name='Total Stone Pieces', default=0)
    total_stone_amount = models.FloatField(verbose_name='Total Stone Amount', default=0.0)
    stone_description = models.CharField(max_length=500, verbose_name='Stone Description', null=True, blank=True)
    total_diamond_weight = models.FloatField(verbose_name='Total Diamond Weight', default=0.0)
    total_diamond_pieces = models.IntegerField(verbose_name='Total Diamond Pieces', default=0)
    total_diamond_amount = models.FloatField(verbose_name='Total Diamond Amount', default=0.0)
    diamond_description = models.CharField(max_length=500, verbose_name='Diamond Description', null=True, blank=True)
    actual_amount = models.FloatField(verbose_name='Actual Amount')
    total_amount = models.FloatField(verbose_name='Total Amount')
    is_assigned = models.BooleanField(verbose_name="Assigned", default=False)
    assigned_by = models.ForeignKey(User, verbose_name='Assigned by', related_name='order_item_assigned_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    is_recieved = models.BooleanField(verbose_name="Recieved", default=False)
    is_delivered = models.BooleanField(verbose_name="Recieved", default=False)
    is_converted_to_lot = models.BooleanField(verbose_name="Convert to lot", default=False)
    delivered_at = models.DateTimeField(verbose_name='Delivered at', null=True, blank=True)
    description = models.CharField(verbose_name="Description", max_length=500, null=True, blank=True)
    order_status = models.ForeignKey(StatusTable, verbose_name='Order Status', related_name="order_item_order_status", on_delete=models.PROTECT, default=settings.PENDING)

    class Meta:
        db_table = 'order_management_order_item'
        verbose_name = 'order_management_order_item'
        verbose_name_plural = 'order_management_order_items'

    def __str__(self) -> str:
        return self.order_id.order_id
    
def content_file_name(instance, filename):
    return '/'.join(['order_management', instance.order_id, instance.order_item, filename])

class OrderItemAttachments(models.Model):

    order_id = models.CharField(verbose_name='Order id', max_length=100)
    order_item = models.CharField(verbose_name='Order Item', max_length=100)
    image = models.FileField(upload_to=content_file_name)

    class Meta:
        db_table = 'order_management_order_item_attachement'
        verbose_name = 'order_management_order_item_attachement'
        verbose_name_plural = 'order_management_order_item_attachements'

class OrderIssue(models.Model):

    order_id = models.ForeignKey(OrderId, verbose_name='Order Id', on_delete=models.CASCADE)
    order_item = models.OneToOneField(OrderItemDetails, verbose_name='Order Item', on_delete=models.PROTECT)
    vendor = models.ForeignKey(AccountHeadDetails, verbose_name='Vendor', on_delete=models.PROTECT)
    issue_date = models.DateField(verbose_name='Issue Date')
    no_of_days = models.IntegerField(verbose_name='No of Days')
    remainder_date = models.DateField(verbose_name='Remainder Date')
    paid_amount=models.FloatField(verbose_name="Paid Amount",null=True,blank=True,default=0)
    paid_weight=models.FloatField(verbose_name="Paid Weight",null=True,blank=True,default=0)
    payment_status = models.ForeignKey(PaymentStatus, verbose_name='Payment Status', related_name="order_item_payment_status", on_delete=models.PROTECT, default=settings.PENDING)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', related_name='order_issue_created_by', on_delete=models.DO_NOTHING)
    modified_by = models.ForeignKey(User, verbose_name='Modified by', related_name='order_issue_modified_by', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'order_management_order_issue'
        verbose_name = 'order_management_order_issue'
        verbose_name_plural = 'order_management_order_issues'

    def __str__(self) -> str:
        return self.vendor.account_head_name
    
