from django.db import models
from customer.models import Customer
from django.conf import settings 
from masters.models import Metal,GSTType
from organizations.models import Branch,User,Staff

# Create your models here.

class OldGoldBillDetails(models.Model):
    
    old_gold_bill_number = models.CharField(max_length=150,verbose_name="Old Gold Bill Number",unique=True)
    customer_details = models.ForeignKey(Customer,verbose_name="Customer",on_delete=models.PROTECT)
    old_gold_weight = models.FloatField(verbose_name="Old_gold_weight",default=0.0)
    old_gold_pieces = models.IntegerField(verbose_name="Old Gold Pieces",default=0)
    gst_type = models.ForeignKey(GSTType,verbose_name="Gst Type",default=1,on_delete=models.PROTECT)
    gst_percent = models.FloatField(verbose_name="Gst Percent",default=0.0)
    total_gst_amount = models.FloatField(verbose_name="Total GST Pieces",default=0.0)
    old_gold_amount = models.FloatField(verbose_name="Old Gold Amount",default=0.0)
    is_billed = models.BooleanField(verbose_name="Billing Status",default=False)
    refference_number = models.CharField(max_length=150,verbose_name="Refference Number",null=True,blank=True)
    is_canceled = models.BooleanField(verbose_name="Status",default=False)
    branch=models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name="Created at",null=True,blank=True)
    created_by = models.ForeignKey(User,verbose_name="Created by",null=True,blank=True,on_delete=models.PROTECT)
    modified_at = models.DateTimeField(verbose_name="Modified at",null=True,blank=True)
    modified_by = models.CharField(max_length=150,verbose_name="Modified by",null=True,blank=True)
  
    class Meta:
        db_table = 'old_gold_bill_details'
        verbose_name = 'old_gold_bill_details'
        verbose_name_plural = 'old_gold_bill_details'
        
    def __str__(self) -> str:
        return self.customer_details.customer_name
    
class OldGoldItemDetails(models.Model):
    
    old_bill_details = models.ForeignKey(OldGoldBillDetails,verbose_name="Old Bill Details",on_delete=models.CASCADE)
    old_metal = models.ForeignKey(Metal,verbose_name="Metal",on_delete=models.PROTECT)
    old_gross_weight = models.FloatField(verbose_name="Old Gross Weight",default=0.0)
    old_reduce_weight = models.FloatField(verbose_name="Old Reduce Weight",default=0.0)
    old_touch = models.FloatField(verbose_name="Old Touch",default=0.0)
    old_rate = models.FloatField(verbose_name="Old Rate",default=0.0)
    old_dust_weight = models.FloatField(verbose_name="Old Dust Weight",default=0.0)
    old_net_weight = models.FloatField(verbose_name="Old Net Weight",default=0.0)
    old_amount = models.FloatField(verbose_name="Old Amount",default=0.0)
    gst_amount = models.FloatField(verbose_name="GST Amount",default=0.0)
    total_amount = models.FloatField(verbose_name="Total Amount",default=0.0)
    is_transffered = models.BooleanField(verbose_name="Transfer status",default=False)
    employee_id = models.ForeignKey(Staff,verbose_name="Employee Id",null=True,blank=True,on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'old_item_details'
        verbose_name = 'old_item_details'
        verbose_name_plural = 'old_item_details'
        
    def __str__(self) -> str:
        return self.old_bill_details.customer_details.customer_name