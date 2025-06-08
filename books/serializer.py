from rest_framework import serializers
from .models import *

class CompanyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=CompanyDetails
        fields="__all__"

class CompanyAddressDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=CompanyAddressDetails
        fields="__all__"

class CompanyBankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=CompanyBankDetails
        fields="__all__"

class CompanyGstDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=CompanyGstDetails
        fields="__all__"

class AccountGroupSerailizer(serializers.ModelSerializer):
    class Meta:
        model=AccountGroup
        fields="__all__"
    
class CustomerTypeSerailizer(serializers.ModelSerializer):
    class Meta:
        model=CustomerType
        fields="__all__"
class AccountTypeSerailizer(serializers.ModelSerializer):
    class Meta:
        model=AccountType
        fields="__all__"

class AccountHeadDetailsSerailizer(serializers.ModelSerializer):
    class Meta:
        model=AccountHeadDetails
        fields="__all__"

class AccountHeadAddressSerailizer(serializers.ModelSerializer):
    class Meta:
        model=AccountHeadAddress
        fields="__all__"

class AccountHeadContactSerailizer(serializers.ModelSerializer):
    class Meta:
        model=AccountHeadContact
        fields="__all__"

class AccountHeadBankDetailsSerailizer(serializers.ModelSerializer):
    class Meta:
        model=AccountHeadBankDetails
        fields="__all__"

class AccountHeadGstDetailsSerailizer(serializers.ModelSerializer):
    class Meta:
        model=AccountHeadGstDetails
        fields="__all__"

