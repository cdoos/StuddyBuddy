from rest_framework import serializers
from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    info_link = serializers.CharField(allow_blank=True)
    verified = serializers.BooleanField(default=True)
    lat = serializers.DecimalField(max_digits=20, decimal_places=10)
    lng = serializers.DecimalField(max_digits=20, decimal_places=10)

    class Meta:
        model = Place
        fields = (
            'name',
            'info_link',
            'verified',
            'lat',
            'lng',
        )
