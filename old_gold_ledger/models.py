from django.conf import settings
from django.db import models
from books.models import AccountHeadDetails
from masters.models import Metal
from organizations.models import User,Branch

# Create your models here.

class OldGoldLedgerType(models.Model):
   
    old_ledger_entry_type = models.CharField(max_length=150,verbose_name="Old Leger Entry Type",unique=True)
    created_at = models.DateTimeField(verbose_name="Created at",null=True,blank=True)
    created_by = models.ForeignKey(User,verbose_name="Created By",on_delete=models.PROTECT)

    class Meta:
        db_table = 'old_ledger_type'
        verbose_name = 'old_ledger_type'
        verbose_name_plural = 'old_ledger_types'
        
    def __str__(self) -> str:
        return self.entry_id

class OldGoldLedger(models.Model):
    
    vendor_details = models.ForeignKey(AccountHeadDetails,verbose_name="Vendor Details",on_delete=models.PROTECT,null=True,blank=True)
    entry_date = models.DateTimeField(verbose_name="Entry Date")
    old_ledger_entry_type = models.CharField(max_length=150,verbose_name="Old Leger Entry Type")
    metal_details = models.ForeignKey(Metal,verbose_name="Metal Details",on_delete=models.PROTECT)
    touch = models.FloatField(verbose_name="Touch",default=0.0)
    weight = models.FloatField(verbose_name="Weight",default=0.0)
    refference_number = models.CharField(max_length=150,verbose_name="Refference Number")
    branch=models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT)
    is_cancelled = models.BooleanField(verbose_name="Cancel Status",default=False)
    created_by = models.CharField(max_length=150,verbose_name="Created By")
    
    class Meta:
        db_table = 'old_gold_leger'
        verbose_name = 'old_gold_leger'
        verbose_name_plural = 'old_gold_leger'
        
    def __str__(self) -> str:
        return self.refference_number
    
class MetalEntries(models.Model):
    
    entry_id = models.CharField(max_length=150,verbose_name="Entry ID",unique=True)
    metal_details = models.ForeignKey(Metal,verbose_name="Metal Details",on_delete=models.PROTECT)
    touch = models.FloatField(verbose_name="Touch",default=0.0)
    weight = models.FloatField(verbose_name="Weight",default=0.0)
    is_cancelled = models.BooleanField(verbose_name="Cancel Status",default=False)
    branch=models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name="Created at",null=True,blank=True)
    created_by = models.CharField(max_length=150,verbose_name="Created by",null=True,blank=True)

    class Meta:
        db_table = 'metal_entries'
        verbose_name = 'metal_entries'
        verbose_name_plural = 'metal_entries'
        
    def __str__(self) -> str:
        return self.entry_id
    
    
    
    
