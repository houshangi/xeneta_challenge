from rest_framework import serializers


class AveragePriceSerializer(serializers.Serializer):
    day = serializers.DateField()
    average_price = serializers.FloatField()
