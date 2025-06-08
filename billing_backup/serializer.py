from rest_framework import serializers
from .models import *


class BillingBackupDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingBackupDetails
        fields = '__all__'

class BillingBackupTagItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingBackupTagItems
        fields = '__all__'

class BillingBackupStoneDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingBackupStoneDetails
        fields = '__all__'

class BillingBackupDiamondDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingBackupDiamondDetails
        fields = '__all__'

class BillingBackupOldGoldSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingBackupOldGold
        fields = '__all__'

class BackupBillIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = BackupBillID
        fields = '__all__'