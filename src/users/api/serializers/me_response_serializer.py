from rest_framework import serializers


class MeResponseSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    email = serializers.EmailField()
