from rest_framework import serializers


class RefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
