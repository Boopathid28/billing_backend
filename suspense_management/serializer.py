from rest_framework import serializers
from .models import *

class SuspenseDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SuspenseDetails
        fields = '__all__'

class SuspenseItemDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SuspenseItemDetails
        fields = '__all__'

class SuspensePaymentDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SuspensePaymentDetails
        fields = '__all__'

class SuspensePaymentDenominationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SuspensePaymentDenominations
        fields = '__all__'