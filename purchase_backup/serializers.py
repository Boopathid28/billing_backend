from rest_framework import serializers
from .models import *

class PurchaseTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseType
        fields = '__all__'

class PurchaseEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseEntry
        fields = '__all__'

class PurchasepaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchasepayment
        fields = '__all__'
        
class PurchaseItemDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseItemDetail
        fields = '__all__'

class PurchaseStoneDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseStoneDetails
        fields = '__all__'

class PurchaseDiamondDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseDiamondDetails
        fields = '__all__'

class NewPurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewPurchase
        fields = '__all__'

class NewPurchaseItemdetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewPurchaseItemdetail
        fields = '__all__'

class NewPurchaseStoneDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewPurchaseStoneDetails
        fields = '__all__'

class NewPurchaseDiamondDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewPurchaseDiamondDetails
        fields = '__all__'
    
class MetalRateCutSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetalRateCut
        fields = '__all__'
    
class CashRateCutSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CashRateCut
        fields = '__all__'

class AmountSettleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AmountSettle
        fields = '__all__'
