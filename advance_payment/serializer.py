from rest_framework import serializers
from .models import *

class AdvancePurposeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdvancePurpose
        fields = '__all__'

class AdvanceDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdvanceDetails
        fields = '__all__'

class AdvanceLogsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdvanceLogs
        fields = '__all__'