from rest_framework import serializers
from .models import *

class MenuGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuGroup
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = '__all__'

class MenuPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuPermission
        fields = '__all__'

class PaymentModeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMode
        fields = '__all__'

class PaymentStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentStatus
        fields = '__all__'

class SaleReturnPolicySerializer(serializers.ModelSerializer):

    class Meta:
        model = SaleReturnPolicy
        fields = '__all__'

class GenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gender
        fields = '__all__'

class PrintModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrintModule
        fields = '__all__'

class MainMenuGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainMenuGroup
        fields = '__all__'
    

class IncentiveTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncentiveType
        fields = '__all__'


class IncentivePercentSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncentivePercent
        fields = '__all__'
       

class SalesEntryTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesEntryType
        fields = '__all__'


class TransactionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransactionType
        fields = '__all__'