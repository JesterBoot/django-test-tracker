from rest_framework import serializers

from users.api.serializers.token_pair_serializer import TokenPairSerializer


class RegisterResponseSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    email = serializers.EmailField()
    tokens = TokenPairSerializer()
