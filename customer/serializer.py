from rest_framework import serializers
from .models import *

class CustomerGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerGroup
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class CustomerLedgerSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerLedger
        fields = '__all__'