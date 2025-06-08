from rest_framework import serializers
from .models import *

class LotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lot
        fields = '__all__'

class LotItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = LotItem
        fields = '__all__'


class LotItemStoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = LotItemStone
        fields = '__all__'

class LotItemDiamondSerializer(serializers.ModelSerializer):

    class Meta:
        model = LotItemDiamond
        fields = '__all__'

class LotIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = LotID
        fields = '__all__'

class TagNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = TagNumber
        fields = '__all__'


class TagEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = TagEntry
        fields = '__all__'

class TaggedItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaggedItems
        fields = '__all__'


class TaggedItemStoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaggedItemStone
        fields = '__all__'


class TaggedItemDiamondSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaggedItemDiamond
        fields = '__all__'

class DuplicateTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = DuplicateTag
        fields = '__all__'
