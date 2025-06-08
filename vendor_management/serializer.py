from rest_framework import serializers
from .models import *

class VendorLedgerSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorLedger
        fields = '__all__'
        
class VendorDiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorDiscount
        fields = '__all__'
        
class VendorPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorPayment
        fields = '__all__'
        
class VendorAmountPaymentDenominationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorAmountPaymentDenominations
        fields = '__all__'
        
class VendorWeightPaymentDenominationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorWeightPaymentDenominations
        fields = '__all__'