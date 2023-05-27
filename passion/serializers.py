from rest_framework import serializers


class PassionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
