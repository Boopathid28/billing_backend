from django.db import models
from accounts.models import User
from books.models import AccountHeadDetails
from masters.models import Metal
from accounts.models import Branch
from settings.models import StatusTable,PaymentStatus
from old_gold_management.models import OldGoldItemDetails

# Create your models here.

class OldMetalCategory(models.Model):
    category_name = models.CharField(max_length=50,verbose_name="Category Name",unique=True)
    
    class Meta:
        db_table = 'old_metal_category'
        verbose_name = 'old_metal_category'
        verbose_name_plural = 'old_metal_categorys'

    def __str__(self) -> str:
        return self.category_name

class BagID(models.Model):
    bag_id =models.CharField(max_length=50,verbose_name=" Bag Id",unique=True)
    
    class Meta:
        db_table = 'bag_id'
        verbose_name = 'bag_id'
        verbose_name_plural = 'bag_id'

    def __str__(self) -> str:
        return self.bag_id
    
class BagNumber(models.Model):
    
    bag_number=models.CharField(max_length=50,verbose_name=" bag Number",unique=True)
    user=models.OneToOneField(User,verbose_name="User",on_delete=models.CASCADE,unique=True)
    class Meta:
        db_table = 'bag_number'
        verbose_name = 'bag_number'
        verbose_name_plural = 'bag_numbers'

    def __str__(self) -> str:
        return self.bag_number
    
class TransferCreationType(models.Model):
    type_name = models.CharField(max_length=50,verbose_name="Type Name",unique= True)
    
    class Meta:
        db_table = 'transfer_creation_type'
        verbose_name = 'transfer_creation_type'
        verbose_name_plural = 'transfer_creation_types'

    def __str__(self) -> str:
        return self.type_name
    

    
class OldGoldType(models.Model):
    type_name = models.CharField(max_length=50,verbose_name="Old Gold Type",unique= True)
    
    class Meta:
        db_table = 'old_gold_type'
        verbose_name = 'old_gold_type'
        verbose_name_plural = 'old_gold_types'

    def __str__(self) -> str:
        return self.type_name
    
    
class TransferCreation(models.Model):
    transfer_type = models.ForeignKey(TransferCreationType,verbose_name="Transfer Type",on_delete=models.PROTECT)
    refference_number = models.CharField(max_length=50,verbose_name="Refference Number",unique=True)
    transfer_category = models.ForeignKey(OldMetalCategory,verbose_name="Trasfer_category",on_delete=models.PROTECT)
    smith = models.ForeignKey(AccountHeadDetails,verbose_name="Smith",on_delete=models.PROTECT)
    total_gross_weight = models.FloatField(max_length=50,verbose_name="Total Gross Weight",default=0.0)
    total_net_weight = models.FloatField(max_length=50,verbose_name="Total Net Weight",default=0.0)
    total_dust_weight = models.FloatField(max_length=50,verbose_name="Total Dust Weight",default=0.0)
    metal=models.ForeignKey(Metal,verbose_name="Metal",on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT)
    is_issued = models.BooleanField(verbose_name="Status",default=False)
    created_by=models.ForeignKey(User,verbose_name="Created By",on_delete=models.DO_NOTHING)
    created_at=models.DateTimeField(verbose_name="Created At",null=True,blank=True)
    
    class Meta:
        db_table = 'transfer_creation'
        verbose_name = 'transfer_creation'
        verbose_name_plural = 'transfer_creations'

    def __str__(self) -> str:
        return self.refference_number
    
class TransferCreationItems(models.Model):
    transfet_creation_details = models.ForeignKey(TransferCreation,verbose_name="Transfer Creation Details",on_delete=models.CASCADE)
    old_item_details = models.ForeignKey(OldGoldItemDetails,verbose_name="Old Gold Item",null=True,blank=True,on_delete=models.PROTECT)
    old_gold_number = models.CharField(max_length=50,verbose_name="Old Gold Number")
    old_metal = models.ForeignKey(Metal,verbose_name="Old Metal",on_delete=models.PROTECT)
    received_date = models.DateField(verbose_name="Received Date")
    transfered_date = models.DateField(verbose_name="Transfered Date")
    gross_weight = models.FloatField(max_length=50,verbose_name="gross weight",null=True,blank=True)
    net_weight = models.FloatField(max_length=50,verbose_name="net weight",null=True,blank=True)
    dust_weight = models.FloatField(max_length=50,verbose_name="dust weight",null=True,blank=True)
    
    class Meta:
        db_table = 'transfer_creation_item'
        verbose_name = 'transfer_creation_item'
        verbose_name_plural = 'transfer_creation_items'

    def __str__(self) -> str:
        return self.old_gold_number
    

    
    
class MeltingIssueID(models.Model):
    melting_issue_id =models.CharField(max_length=50,verbose_name=" melting issue Id",unique=True)
    
    class Meta:
        db_table = 'melting_issue_id'
        verbose_name = 'melting_issue_id'
        verbose_name_plural = 'melting_issue_id'

    def __str__(self) -> str:
        return self.melting_issue_id
    
class MeltingIssueNumber(models.Model):
    
    melting_issue_number=models.CharField(max_length=50,verbose_name=" melting issue Number",unique=True)
    user=models.OneToOneField(User,verbose_name="User",on_delete=models.CASCADE,unique=True)
    class Meta:
        db_table = 'melting_issue_number'
        verbose_name = 'melting_issue_number'
        verbose_name_plural = 'melting_issue_numbers'

    def __str__(self) -> str:
        return self.melting_issue_number
    
class MeltingIssue(models.Model):
    
    transfer_creation_details = models.OneToOneField(TransferCreation,verbose_name="Transfer creation Details",on_delete=models.PROTECT,unique=True)
    melting_issue_id = models.CharField(max_length=50,verbose_name="Melting Issue ID")
    vendor_details = models.ForeignKey(AccountHeadDetails,verbose_name="Vendor Details",on_delete=models.PROTECT,null=True)
    metal_details = models.ForeignKey(Metal,verbose_name="Metal Details",on_delete=models.PROTECT,null=True)
    issued_category = models.ForeignKey(OldMetalCategory,verbose_name="Issued Category",on_delete=models.PROTECT)
    issued_date = models.DateField(verbose_name="Issued Date")
    return_days = models.IntegerField(verbose_name="Due Days")
    return_date = models.DateField(verbose_name="Issued Date")
    bullion_rate = models.FloatField(max_length=50,verbose_name="Bullion Rate",default=0.0)
    stone_weight = models.FloatField(max_length=50,verbose_name="Stone Weight",default=0.0)
    gross_weight = models.FloatField(max_length=50,verbose_name="Stone Weight",default=0.0)
    net_weight = models.FloatField(max_length=50,verbose_name="Stone Weight",default=0.0)
    melting_status = models.ForeignKey(StatusTable,verbose_name="Melting Status",on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT)
    notes = models.TextField(verbose_name="Notes",null=True,blank=True)
    issued_by=models.ForeignKey(User,verbose_name="issued By",on_delete=models.DO_NOTHING)
    issued_at=models.DateTimeField(verbose_name="issued At",null=True,blank=True)
    is_received = models.BooleanField(verbose_name="Status",default=False)
    is_issued = models.BooleanField(verbose_name="Issue status",default=False)
    is_cancelled = models.BooleanField(verbose_name="Cancel status",default=False)
    
    class Meta:
        db_table = 'melting_issue'
        verbose_name = 'melting_issue'
        verbose_name_plural = 'melting_issues'

    def __str__(self) -> str:
        return self.melting_issue_id
    
class MeltingReciptID(models.Model):
    melting_recipt_id =models.CharField(max_length=50,verbose_name=" melting recipt Id",unique=True)
    
    class Meta:
        db_table = 'melting_recipt_id'
        verbose_name = 'melting_recipt_id'
        verbose_name_plural = 'melting_recipt_id'

    def __str__(self) -> str:
        return self.melting_recipt_id
    
class MeltingReciptNumber(models.Model):
    
    melting_recipt_number=models.CharField(max_length=50,verbose_name=" melting recipt Number",unique=True)
    user=models.OneToOneField(User,verbose_name="User",on_delete=models.CASCADE,unique=True)
    class Meta:
        db_table = 'melting_recipt_number'
        verbose_name = 'melting_recipt_number'
        verbose_name_plural = 'melting_recipt_numbers'

    def __str__(self) -> str:
        return self.melting_recipt_number
    
class MeltingRecipt(models.Model):
    
    melting_issue_details = models.OneToOneField(MeltingIssue,verbose_name="Melting Issue Details",on_delete=models.PROTECT,unique=True)
    melting_recipt_id = models.CharField(max_length=50,verbose_name="Melting Recipt ID")
    vendor_details = models.ForeignKey(AccountHeadDetails,verbose_name="Vendor Details",on_delete=models.PROTECT,null=True)
    received_category = models.ForeignKey(OldMetalCategory,verbose_name="Received Category",on_delete=models.PROTECT)
    received_date = models.DateField(verbose_name="received Date")
    melting_loss_weight = models.FloatField(max_length=50,verbose_name="Melting Loss Weight",default=0.0)
    recipt_net_weight = models.FloatField(max_length=50,verbose_name="Recipt Net Weight",default=0.0)
    melting_charges = models.FloatField(max_length=50,verbose_name="Melting Charges",default=0.0)
    amount_paid = models.FloatField(max_length=50,verbose_name="Amount Paid",default=0.0)
    payment_status = models.ForeignKey(PaymentStatus,verbose_name="Payment Status",related_name="melting_payment_status",on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT)
    remark = models.TextField(verbose_name="Remark",null=True,blank=True)
    melting_status = models.ForeignKey(StatusTable,verbose_name="Melting Status",related_name="melting_status",on_delete=models.PROTECT)
    received_by=models.ForeignKey(User,verbose_name="received By",on_delete=models.DO_NOTHING)
    received_at=models.DateTimeField(verbose_name="received At",null=True,blank=True)
    is_cancelled = models.BooleanField(verbose_name="Cancel status",default=False)
    
    class Meta:
        db_table = 'melting_recipt'
        verbose_name = 'melting_recipt'
        verbose_name_plural = 'melting_recipts'

    def __str__(self) -> str:
        return self.melting_recipt_id
    
class PurificationIssueID(models.Model):
    purification_issue_id =models.CharField(max_length=50,verbose_name=" Purification Issue Id",unique=True)
    
    class Meta:
        db_table = 'purification_issue_id'
        verbose_name = 'purification_issue_id'
        verbose_name_plural = 'purification_issue_ids'

    def __str__(self) -> str:
        return self.purification_issue_id
    
class PurificationIssueNumber(models.Model):
    
    purification_issue_number=models.CharField(max_length=50,verbose_name="Purification Issue Number",unique=True)
    user=models.OneToOneField(User,verbose_name="User",on_delete=models.CASCADE,unique=True)
    class Meta:
        db_table = 'purification_issue_number'
        verbose_name = 'purification_issue_number'
        verbose_name_plural = 'purification_issue_numbers'

    def __str__(self) -> str:
        return self.purification_issue_number
    
class PurificationIssue(models.Model):
    melting_recipt_details = models.OneToOneField(MeltingRecipt,verbose_name="Melting Recipt Details",on_delete=models.PROTECT)
    purification_issue_id = models.CharField(max_length=100,verbose_name="Purification Issue Id",unique=True)
    smith = models.ForeignKey(AccountHeadDetails,verbose_name="Smith Details",on_delete=models.PROTECT,null=True)
    metal_details = models.ForeignKey(Metal,verbose_name="Metal Details",on_delete=models.PROTECT,null=True)
    issued_category = models.ForeignKey(OldMetalCategory,verbose_name="Issued Category",on_delete=models.PROTECT)
    issued_date = models.DateField(verbose_name="Issued Date")
    return_days = models.IntegerField(verbose_name="Due Days")
    return_date = models.DateField(verbose_name="Return Date")
    bag_weight = models.FloatField(max_length=50,verbose_name="Bag Weight",default=0.0)
    recipt_metal_weight = models.FloatField(max_length=50,verbose_name="Recipt Metal Weight",default=0.0)
    issued_pure_weight = models.FloatField(max_length=50,verbose_name="Issued Pure Weight",default=0.0)
    purification_status = models.ForeignKey(StatusTable,verbose_name="Purification Status",on_delete=models.PROTECT)
    notes = models.TextField(verbose_name="Notes",null=True,blank=True)
    branch = models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT)
    issued_by=models.ForeignKey(User,verbose_name="issued By",on_delete=models.DO_NOTHING,null=True,blank=True)
    issued_at=models.DateTimeField(verbose_name="issued At",null=True,blank=True)
    is_received = models.BooleanField(verbose_name="Status",default=False)
    is_issued = models.BooleanField(verbose_name="Issue status",default=False)
    is_cancelled = models.BooleanField(verbose_name="Cancel status",default=False)
    
    class Meta:
        db_table = 'purification_issue'
        verbose_name = 'purification_issue'
        verbose_name_plural = 'purification_issues'

    def __str__(self) -> str:
        return self.purification_issue_id
    
class PurificationReciptID(models.Model):
    purification_recipt_id =models.CharField(max_length=50,verbose_name=" Purification recipt Id",unique=True)
    
    class Meta:
        db_table = 'purification_recipt_id'
        verbose_name = 'purification_recipt_id'
        verbose_name_plural = 'purification_recipt_ids'

    def __str__(self) -> str:
        return self.purification_recipt_id
    
class PurificationReciptNumber(models.Model):
    
    purification_recipt_number=models.CharField(max_length=50,verbose_name="Purification recipt Number",unique=True)
    user=models.OneToOneField(User,verbose_name="User",on_delete=models.CASCADE,unique=True)
    class Meta:
        db_table = 'purification_recipt_number'
        verbose_name = 'purification_recipt_number'
        verbose_name_plural = 'purification_recipt_numbers'

    def __str__(self) -> str:
        return self.purification_recipt_number
    
class PurificationRecipt(models.Model):
    purification_issue_details=models.OneToOneField(PurificationIssue,verbose_name="Purification Issue Details",on_delete=models.PROTECT)
    putification_recipt_id = models.CharField(max_length=50,verbose_name="Purification Recipt Id",unique=True)
    metal_details = models.ForeignKey(Metal,verbose_name="Metal Details",on_delete=models.PROTECT,null=True)
    received_date = models.DateField(verbose_name="Recived Date")
    vendor_details = models.ForeignKey(AccountHeadDetails,verbose_name="Vendor Details",on_delete=models.PROTECT,null=True)
    received_category = models.ForeignKey(OldMetalCategory,verbose_name="Received Category",on_delete=models.PROTECT)
    issued_weight = models.FloatField(max_length=50,verbose_name="Issued Weight",default=0.0)
    issued_pure_weight = models.FloatField(max_length=50,verbose_name="Issued Pure Weight",default=0.0)
    received_pure_weight = models.FloatField(max_length=50,verbose_name="Received Pure Weight",default=0.0)
    touch = models.FloatField(max_length=50,verbose_name="Touch",default=0.0)
    melting_bullion_rate = models.FloatField(max_length=50,verbose_name="Melting Bullion Rate",default=0.0)
    purification_charges = models.FloatField(max_length=50,verbose_name="Purification Charges",default=0.0)
    amount_paid = models.FloatField(max_length=50,verbose_name="Paid Amount",default=0.0)
    payment_status = models.ForeignKey(PaymentStatus,verbose_name="Payment Status",on_delete=models.PROTECT,related_name="payment_status")
    purification_status = models.ForeignKey(StatusTable,verbose_name="Purification Status",on_delete=models.PROTECT,related_name="purification_status")
    branch = models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT)
    received_by=models.ForeignKey(User,verbose_name="received By",on_delete=models.DO_NOTHING,null=True,blank=True)
    received_at=models.DateTimeField(verbose_name="received At",null=True,blank=True)
    is_cancelled = models.BooleanField(verbose_name="Cancel status",default=False)
    
    
    class Meta:
        db_table = 'purification_recipt'
        verbose_name = 'purification_recipt'
        verbose_name_plural = 'purification_recipts'

    def __str__(self) -> str:
        return self.putification_recipt_id
    
    
    
    
    