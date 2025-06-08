from django.db import models
from accounts.models import *
from organizations.models import *
from tagging.models import TaggedItems,EntryType
from customer.models import Customer
from settings.models import StatusTable
from billing.models import *


class TransferStatus(models.Model):
    status_name=models.CharField(max_length=50,verbose_name="transfer_status_name")
    status_comments=models.CharField(max_length=50,verbose_name="transfer_status_comments")
    status_bgcolor=models.CharField(max_length=255,verbose_name="transfer_bg_color", null=True, blank=True)
    status_color=models.CharField(max_length=255,verbose_name="transfer_status_color", null=True, blank=True)
    created_at=models.DateTimeField(verbose_name='transferstatus_Created at', null=True, blank=True)
    created_by=models.ForeignKey(User, verbose_name='transferstatus_Created by', on_delete=models.DO_NOTHING)
    modified_at=models.DateTimeField(verbose_name='transferstatus_Modified at', null=True, blank=True)
    modified_by= models.IntegerField(verbose_name='transferstatus_Modified by', null=True, blank=True)

    class Meta:
        db_table = 'transferstatus'
        verbose_name = 'transferstatus'
        verbose_name_plural = 'transferstatus'

    def __str__(self) -> str:
        return self.status_name


class TransferType(models.Model):
    status_name=models.CharField(max_length=50,verbose_name="transfer_type_name")
    created_at=models.DateTimeField(verbose_name='transfer_type_Created at', null=True, blank=True)
    created_by=models.ForeignKey(User, verbose_name='transfer_type_Created by', on_delete=models.DO_NOTHING)
    modified_at=models.DateTimeField(verbose_name='transfer_type_Modified at', null=True, blank=True)
    modified_by= models.IntegerField(verbose_name='transfer_type_Modified by', null=True, blank=True)

    class Meta:
        db_table = 'transfer_type'
        verbose_name = 'transfer_type'
        verbose_name_plural = 'transfer_type'

    def __str__(self) -> str:
        return self.status_name

class TransferItem(models.Model):
    transfer_date=models.DateField(verbose_name="transfer date")
    required_date=models.DateField(verbose_name="required date")
    transfer_from = models.ForeignKey(Branch,related_name="transfer_from_branch", on_delete=models.DO_NOTHING,db_column='transfer_from')
    transfer_to =models.ForeignKey(Branch,related_name="transfer_to_branch", on_delete=models.DO_NOTHING,db_column='transfer_to')
    stock_authority=models.ForeignKey(Staff,related_name="stock_authority_staff", on_delete=models.DO_NOTHING,db_column='stock_authority')   
    transfer_status= models.ForeignKey(TransferStatus,related_name="transfer_item_status", on_delete=models.DO_NOTHING,db_column='transfer_status')   
    created_at=models.DateTimeField(verbose_name='transfer_Created at', null=True, blank=True)
    created_by=models.ForeignKey(User, verbose_name='transfer_Created by', on_delete=models.DO_NOTHING)
    modified_at=models.DateTimeField(verbose_name='transfer_Modified at', null=True, blank=True)
    modified_by= models.IntegerField(verbose_name='transfer_Modified by', null=True, blank=True)

    class Meta:
        db_table = 'transerfer_items'
        verbose_name = 'transerfer_item'
        verbose_name_plural = 'transerfer_items'
 
    def __str__(self) -> str:
        return str(self.id)

class TransferItemDetails(models.Model):
    transfer_itemid=models.ForeignKey(TransferItem,related_name="transfer_details_transfer_id", on_delete=models.DO_NOTHING,db_column='transfer_itemid')
    tagitems_id=models.ForeignKey(TaggedItems,related_name="transfer_details_tag_item_id", on_delete=models.DO_NOTHING)
    tag_number=models.CharField(max_length=255,verbose_name="transfer_details_tag_number")
    created_at=models.DateTimeField(verbose_name='transfer_details_Created at', null=True, blank=True)
    created_by=models.ForeignKey(User, verbose_name='transfer_details_Created by', on_delete=models.DO_NOTHING)
    modified_at=models.DateTimeField(verbose_name='transfer_details_Modified at', null=True, blank=True)
    modified_by= models.IntegerField(verbose_name='transfer_details_Modified by', null=True, blank=True)

    class Meta:
        db_table = 'transferitem_details'
        verbose_name = 'transferitem_detail'
        verbose_name_plural = 'transferitem_details'
 
    def __str__(self):
        return str(self.id)
    

class ReceivedItem(models.Model):
    transfer_itemid=models.ForeignKey(TransferItem,related_name="received_item_transfer_id", on_delete=models.DO_NOTHING,db_column='transfer_itemid', null=True, blank=True)
    received_date=models.DateField(verbose_name="received_item_transfer date", null=True, blank=True)    
    transfer_status= models.ForeignKey(TransferStatus,related_name="reveive_transfer_item_status", on_delete=models.DO_NOTHING,db_column='transfer_status')   
    created_at=models.DateTimeField(verbose_name='received_item_Created at', null=True, blank=True)
    created_by=models.ForeignKey(User, verbose_name='received_item_Created by', on_delete=models.DO_NOTHING)
    modified_at=models.DateTimeField(verbose_name='received_item_Modified at', null=True, blank=True)
    modified_by= models.IntegerField(verbose_name='received_item_Modified by', null=True, blank=True)

    class Meta:
        db_table = 'received_items'
        verbose_name = 'received_item'
        verbose_name_plural = 'received_items'
 
    def __str__(self) -> str:
        return self.id



class ReceivedItemDetails(models.Model):
    received_itemid=models.ForeignKey(ReceivedItem,related_name="received_item_details_recived_id", on_delete=models.DO_NOTHING,db_column='received_itemid')
    transfer_itemid=models.ForeignKey(TransferItem,related_name="received_item_details_transfer_id", on_delete=models.DO_NOTHING,db_column='transfer_itemid')
    tagitems_id=models.ForeignKey(TaggedItems,related_name="received_item_details_tag_item_id", on_delete=models.DO_NOTHING,db_column='tagitems_id')
    tag_number=models.CharField(max_length=255,verbose_name="received_item_details_tag_number")
    created_at=models.DateTimeField(verbose_name='received_item_details_Created at', null=True, blank=True)
    created_by=models.ForeignKey(User, verbose_name='received_item_details_Created by', on_delete=models.DO_NOTHING)
    modified_at=models.DateTimeField(verbose_name='received_item_details_Modified at', null=True, blank=True)
    modified_by= models.IntegerField(verbose_name='received_item_details_Modified by', null=True, blank=True)

    class Meta:
        db_table = 'receiveditem_details'
        verbose_name = 'receiveditem_detail'
        verbose_name_plural = 'receiveditem_details'
 
    def __str__(self) -> str:
        return self.id
    
class ReturnItem(models.Model):
    transfer_itemid=models.ForeignKey(TransferItem,related_name="return_Item_transfer_id", on_delete=models.DO_NOTHING,db_column='transfer_itemid')
    return_date=models.DateTimeField(verbose_name="return_Item_transfer date")    
    reason=models.TextField(verbose_name="Returnreason", null=True, blank=True)
    transfer_status= models.ForeignKey(TransferStatus,related_name="return_transfer_item_status", on_delete=models.DO_NOTHING,db_column='transfer_status') 
    created_at=models.DateTimeField(verbose_name='return_Item_Created at', null=True, blank=True)
    created_by=models.ForeignKey(User, verbose_name='return_Item_Created by', on_delete=models.DO_NOTHING)
    modified_at=models.DateTimeField(verbose_name='return_Item_Modified at', null=True, blank=True)
    modified_by= models.IntegerField(verbose_name='return_Item_Modified by', null=True, blank=True)

    class Meta:
        db_table = 'return_items'
        verbose_name = 'return_item'
        verbose_name_plural = 'return_items'
 
    def __str__(self) -> str:
        return self.id



class ReturnItemDetails(models.Model):
    return_itemid=models.ForeignKey(ReturnItem,related_name="returnItem_details_recived_id", on_delete=models.DO_NOTHING,db_column='return_itemid')
    transfer_itemid=models.ForeignKey(TransferItem,related_name="returnItem_details_transfer_id", on_delete=models.DO_NOTHING,db_column='transfer_itemid')
    tagitems_id=models.ForeignKey(TaggedItems,related_name="returnItem_details_tag_item_id", on_delete=models.DO_NOTHING,db_column='tagitems_id')
    tag_number=models.CharField(max_length=255,verbose_name="returnItem_details_tag_number")
    created_at=models.DateTimeField(verbose_name='returnItem_details_Created at', null=True, blank=True)
    created_by=models.ForeignKey(User, verbose_name='returnItem_details_Created by', on_delete=models.DO_NOTHING)
    modified_at=models.DateTimeField(verbose_name='returnItem_details_Modified at', null=True, blank=True)
    modified_by= models.IntegerField(verbose_name='returnItem_details_Modified by', null=True, blank=True)

    class Meta:
        db_table = 'returnitem_details'
        verbose_name = 'returnitem_detail'
        verbose_name_plural = 'returnitem_details'
 
    def __str__(self) -> str:
        return self.id
    

class ApprovalIssue(models.Model):
    approval_issue_id = models.CharField(max_length=50,verbose_name="Approval Issue ID",unique=True)
    bill_type = models.ForeignKey(BillingType,verbose_name="Bill Type",on_delete=models.PROTECT)
    estimation_details = models.ForeignKey(EstimateDetails,verbose_name="Estimation Details",on_delete=models.PROTECT,null=True, blank=True)
    issue_date = models.DateField(verbose_name="Issued Date")
    issued_by = models.CharField(max_length=150,verbose_name="Issue By")
    shop_name = models.ForeignKey(Customer,verbose_name="Shop Name",on_delete=models.PROTECT)
    receiver_name = models.CharField(max_length=150,verbose_name="Receiver Name")
    notes = models.TextField(verbose_name="Notes",null=True,blank="True")
    branch = models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT)
    issued_gross_weight = models.FloatField(max_length=100,verbose_name="Issued Gross Weight",default=0.0)
    issued_net_weight = models.FloatField(max_length=100,verbose_name="Issued Net Weight",default=0.0)
    recieved_date = models.DateField(verbose_name="Received Date",null=True,blank=True)
    received_by = models.CharField(max_length=150,verbose_name="Received By",null=True,blank=True)
    received_gross_weight = models.FloatField(max_length=150,verbose_name="Received Gross Weight",default=0.0)
    received_net_weight = models.FloatField(max_length=150,verbose_name="Received Net Weight",default=0.0)
    sold_gross_weight = models.FloatField(max_length=150,verbose_name="Sold Gross Weight",default=0.0)
    sold_net_weight = models.FloatField(max_length=150,verbose_name="Sold Net Weight",default=0.0)
    status = models.ForeignKey(StatusTable,verbose_name="Approval Status",on_delete=models.PROTECT)
    created_at=models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    created_by=models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING)
    modified_at=models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    modified_by= models.IntegerField(verbose_name='Modified by', null=True, blank=True)
    
    class Meta:
        db_table = 'approval_issue'
        verbose_name = 'approval_issue'
        verbose_name_plural = 'approval_issues'
 
    def __str__(self) -> str:
        return self.approval_issue_id
    
class ApprovalIssueTagItems(models.Model):
    approval_issue_details = models.ForeignKey(ApprovalIssue,verbose_name="Approval Issue Details",on_delete=models.CASCADE)
    tag_details = models.ForeignKey(TaggedItems,verbose_name="Tag Details",on_delete=models.PROTECT)
    is_received = models.BooleanField(verbose_name="Received Status",default=False)
    is_sold = models.BooleanField(verbose_name="Sales Status",default=False)
    
    class Meta:
        db_table = 'approval_issue_tag_item'
        verbose_name = 'approval_issue_tag_item'
        verbose_name_plural = 'approval_issue_tag_items'
 
    def __str__(self) -> str:
        return self.approval_issue_details.approval_issue_id
    

class ApprovalIssueNumber(models.Model):
    
    approval_issue_number=models.CharField(max_length=50,verbose_name="Approval Issue Number",unique=True)
    user=models.OneToOneField(User,verbose_name="User",on_delete=models.CASCADE,unique=True)
    class Meta:
        db_table = 'approval_issue_number'
        verbose_name = 'approval_issue_number'
        verbose_name_plural = 'approval_issue_numbers'

    def __str__(self) -> str:
        return self.approval_issue_number 
    
class ApprovalIssueID(models.Model):
    
    approval_issue_id=models.CharField(max_length=50,verbose_name="Silver Bill Id",unique=True)
    
    class Meta:
        db_table = 'approval_issue_id'
        verbose_name = 'approval_issue_id'
        verbose_name_plural = 'approval_issue_id'

    def __str__(self) -> str:
        return self.approval_issue_id


class StockLedgerType(models.Model):
    
    stock_ledger_type = models.CharField(max_length=100,verbose_name="Stock Ledger Type",unique=True)
    created_at=models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    created_by=models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING)
    
    class Meta:
            db_table = 'stock_ledger_type'
            verbose_name = 'stock_ledger_type'
            verbose_name_plural = 'stock_ledger_types'

    def __str__(self) -> str:
        return self.stock_ledger_type
    

class StockLedger(models.Model):
    
    tag_details = models.ForeignKey(TaggedItems,verbose_name="Tag Details",on_delete=models.CASCADE)
    stock_type = models.ForeignKey(StockLedgerType,verbose_name="Stock type",default=2,on_delete=models.PROTECT)
    entry_type = models.ForeignKey(EntryType,verbose_name="Entry Type",default=1,null=True,blank=True,on_delete=models.PROTECT)
    entry_date = models.DateTimeField(verbose_name="Entry Date")
    pieces = models.IntegerField(verbose_name="Pieces",default=0)
    gross_weight = models.FloatField(verbose_name="Gross Weight",default=0.0)
    
    class Meta:
            db_table = 'stock_ledger'
            verbose_name = 'stock_ledger'
            verbose_name_plural = 'stock_ledger'

    def __str__(self) -> str:
        return self.tag_details.tag_number