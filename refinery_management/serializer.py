from rest_framework import serializers
from .models import *


class TransferCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransferCreation
        fields = '__all__'
        
class TransferCreationItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransferCreationItems
        fields = '__all__'
        
class MeltingIssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeltingIssue
        fields = '__all__'
        
class MeltingReciptSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeltingRecipt
        fields = '__all__'
        
class PurificationIssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurificationIssue
        fields = '__all__'
class PurificationReciptSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurificationRecipt
        fields = '__all__'