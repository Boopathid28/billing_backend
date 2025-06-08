from rest_framework import serializers
from .models import *


class ValueAdditionCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = ValueAdditionCustomer
        fields = '__all__'

class ValueAdditionDesignerSerializer(serializers.ModelSerializer):

    class Meta:
        model = ValueAdditionDesigner
        fields = '__all__'

class FlatWastageTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlatWastageType
        fields = '__all__'