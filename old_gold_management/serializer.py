from rest_framework import serializers
from .models import *


class OldGoldBillDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OldGoldBillDetails
        fields = '__all__'

class OldGoldItemDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OldGoldItemDetails
        fields = '__all__'