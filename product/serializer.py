from rest_framework import serializers
from .models import *
class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'

class FixedRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FixedRate
        fields = '__all__'

class WeightCalculationSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeightCalculation
        fields = '__all__'

class PerGramRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PerGramRate
        fields = '__all__'

class SubItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubItem
        fields = '__all__'

class SubItemFixedRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubItemFixedRate
        fields = '__all__'

class SubItemWeightCalculationSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubItemWeightCalculation
        fields = '__all__'

class SubItemPerGramRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubItemPerGramRate
        fields = '__all__'


class ItemIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemID
        fields = '__all__'

class SubItemIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubItemID
        fields = '__all__'

class PerPieceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PerPiece
        fields = '__all__'

class SubItemPerPieceSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubItemPerPiece
        fields = '__all__'