from rest_framework import serializers
from .models import *

class RepairDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepairDetails
        fields = '__all__'

class RepairItemDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepairItemDetails
        fields = '__all__'

class RepairOrderNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepairOrderNumber
        fields = '__all__'

class RepairForSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepairFor
        fields = '__all__'

class RepairOrderIssuedSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepairOrderIssued
        fields = '__all__'

class DeliveryBillSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryBill
        fields = '__all__'

class RepairOrderOldGoldSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepairOrderOldGold
        fields = '__all__'


class RepairPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepairPayment
        fields = '__all__'

class RepairPaymentDenominationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepairPaymentDenominations
        fields = '__all__'

class RepairAdvanceDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepairAdvanceDetails
        fields = '__all__'