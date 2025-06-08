from rest_framework import serializers
from .models import *


class ApprovalTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApprovalType
        fields = '__all__'

class ApprovalRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApprovalRule
        fields = '__all__'