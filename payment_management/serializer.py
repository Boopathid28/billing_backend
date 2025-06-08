from rest_framework import serializers
from .models import *

class CustomerPaymentTabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPaymentTabel
        fields = '__all__'

class PaymentMenthodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMenthod
        fields = '__all__'

class PaymentProvidersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentProviders
        fields = '__all__'

class CommonPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonPaymentDetails
        fields = '__all__'

class PaymentModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentModule
        fields = '__all__'