from rest_framework import serializers
from .models import *



class TransferItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransferItem
        fields = '__all__'

class TransferItemDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransferItemDetails
        fields = '__all__'

class ReceivedItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReceivedItem
        fields = '__all__'

class ReceivedItemDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReceivedItemDetails
        fields = '__all__'

class ReturnItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReturnItem
        fields = '__all__'

class ReturnItemDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReturnItemDetails
        fields = '__all__'


class TransferStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransferStatus
        fields = '__all__'

class TransferTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransferType
        fields = '__all__'
        
        
class ApprovalIssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApprovalIssue
        fields = '__all__'
        
class ApprovalIssueTagItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApprovalIssueTagItems
        fields = '__all__'


class StockLedgerSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockLedger
        fields = '__all__'