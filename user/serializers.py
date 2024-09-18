from typing import Dict

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from user.models import User, BlockUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate_email(self, value: str) -> str:
        value = value.lower()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(["user with this email already exists."])
        return value.lower()

    def create(self, validated_data: Dict[str, str]) -> User:
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']


class BlockUserSerializer(serializers.ModelSerializer):
    blocker = serializers.HiddenField(default=serializers.CurrentUserDefault())
    blocked = serializers.StringRelatedField()
    blocked_id = serializers.IntegerField(required=True, allow_null=False)

    def validate(self, validated_data: Dict) -> Dict:
        validated_data = super(BlockUserSerializer, self).validate(validated_data)
        blocker = validated_data.get("blocker")
        blocked_id = validated_data.get("blocked_id")
        get_object_or_404(BlockUser, id=blocked_id)
        if blocker.id == blocked_id:
            raise serializers.ValidationError({'blocked_id': ["You can't block yourself."]})
        if blocker.blocked_by.filter(blocked_id=blocked_id).exists():
            raise serializers.ValidationError({'blocked_id': ["This user is already blocked."]})
        return validated_data

    class Meta:
        model = BlockUser
        fields = ['blocker', 'blocked_id', 'blocked']
