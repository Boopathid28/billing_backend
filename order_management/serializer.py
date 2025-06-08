from rest_framework import serializers
from .models import *

class OrderForSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFor
        fields = '__all__'

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = '__all__'

class OrderIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderId
        fields = '__all__'

class SessionOrderIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionOrderId
        fields = '__all__'

class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__'

class OrderItemDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemDetails
        fields = '__all__'

class OrderItemAttachmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemAttachments
        fields = '__all__'

class OrderIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderIssue
        fields = '__all__'

