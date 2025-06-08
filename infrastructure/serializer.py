from rest_framework import serializers
from .models import *

class FloorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Floor
        fields = '__all__'

class CounterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Counter
        fields = '__all__'


class CounterTargetSerializer(serializers.ModelSerializer):

    class Meta:
        model = CounterTarget
        fields = '__all__'