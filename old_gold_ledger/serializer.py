from rest_framework import serializers
from .models import *

class OldGoldLedgerSerializer(serializers.ModelSerializer):

    class Meta:
        model = OldGoldLedger
        fields = '__all__'

class MetalEntriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = MetalEntries
        fields = '__all__'