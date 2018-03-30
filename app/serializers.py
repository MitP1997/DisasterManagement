from .models import *
from rest_framework import serializers

class CivilianSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Civilians
        fields = ('first_name',)

class ShelterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shelter
        fields = ('name',)
