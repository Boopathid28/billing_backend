from rest_framework import serializers
from .models import *
from product.models import RangeStock

class MetalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Metal
        fields = '__all__'

class PuritySerializer(serializers.ModelSerializer):

    class Meta:
        model = Purity
        fields = '__all__'

class MetalRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = MetalRate
        fields = '__all__'

class TaxDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaxDetails
        fields = '__all__'

class PurchaseTaxDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseTaxDetails
        fields = '__all__'

class SalesTaxDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesTaxDetails
        fields = '__all__'

class ShapeDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShapeDetails
        fields = '__all__'

class CutDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CutDetails
        fields = '__all__'

class ColorDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ColorDetails
        fields = '__all__'

class ClarityDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClarityDetails
        fields = '__all__'

class CentGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = CentGroup
        fields = '__all__'

class TagTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TagTypes
        fields = '__all__'

class StoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoneDetails
        fields = '__all__'

class CaratRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CaratRate
        fields = '__all__'


class RangeStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = RangeStock
        fields = '__all__'


class OldMetalRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = MetalOldRate
        fields = '__all__'


class RepairTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepairType
        fields = '__all__'

class VoucherTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = VoucherType
        fields = '__all__'

class GiftVoucherSerializer(serializers.ModelSerializer):

    class Meta:
        model = GiftVoucher
        fields = '__all__'

class GSTTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = GSTType
        fields = '__all__'

class TaxDetailsAuditSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaxDetailsAudit
        fields = '__all__'

class CashCounterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CashCounter
        fields = '__all__'