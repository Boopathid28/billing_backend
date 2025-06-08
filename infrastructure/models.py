from django.db import models
from accounts.models import *

class Floor(models.Model):
    floor_name = models.CharField(max_length=100, verbose_name="Floor name")
    branch = models.ForeignKey(Branch, verbose_name="Branch", on_delete=models.PROTECT)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.SET_DEFAULT, default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'floors'
        verbose_name = 'floor'
        verbose_name_plural = 'floors'

    def __str__(self) -> str:
        return self.floor_name
    

class Counter(models.Model):
    counter_name = models.CharField(max_length=100, verbose_name="Counter name")
    floor = models.ForeignKey(Floor, verbose_name="Floor", on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, verbose_name="Branch", on_delete=models.PROTECT)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.SET_DEFAULT, default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'counters'
        verbose_name = 'counter'
        verbose_name_plural = 'counters'

    def __str__(self) -> str:
        return self.counter_name
    
class CounterTarget(models.Model):
    branch = models.ForeignKey(Branch,verbose_name="Branch",on_delete =models.PROTECT,null=True,blank=True)
    counter_details = models.ForeignKey(Counter,verbose_name="Counter Details",on_delete=models.PROTECT)
    target_from_date = models.DateField(verbose_name="Target From Date", null=True,blank = True)
    target_to_date = models.DateField(verbose_name="Target To Date", null=True,blank = True)
    target_pieces = models.IntegerField(verbose_name="Target Pieces",default=0)
    target_weight = models.FloatField(max_length=50,verbose_name="Target Weight",default=0.0)
    target_amount = models.FloatField(max_length=50,verbose_name="Target Amount",default=0.0)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.SET_DEFAULT, default=1)
    

    class Meta:
        db_table = 'counter_target'
        verbose_name = 'counter_target'
        verbose_name_plural = 'counter_targets'

    def __str__(self) -> str:
        return f"{self.counter_details.counter_name}"

    

    