from datetime import timedelta
from typing import Dict

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from friend_request.models import FriendRequest
from user.models import User


class FriendRequestSentSerializer(serializers.ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    receiver = serializers.StringRelatedField(read_only=True)
    status = serializers.ReadOnlyField()
    receiver_id = serializers.IntegerField(required=True, allow_null=False)

    def validate_receiver_id(self, value: int) -> int:
        get_object_or_404(User, pk=value)
        return value

    def validate(self, validated_data: Dict) -> Dict:
        receiver_id = validated_data.get("receiver_id")
        receiver = User.objects.get(id=receiver_id)
        sender = validated_data.get("sender")

        if sender.id == receiver_id:
            raise serializers.ValidationError({'receiver_id': 'Sender is same as Receiver.'})

        if sender.friends.filter(id=receiver_id).exists():
            raise serializers.ValidationError({'receiver_id': 'User is already your friend.'})

        if sender.blocked.filter(blocker_id=receiver_id).exists():
            raise serializers.ValidationError({'receiver_id': f'{receiver} has blocked you.'})

        if FriendRequest.objects.filter(receiver_id=receiver_id, sender_id=sender.id).exists():
            last_request = FriendRequest.objects.get(receiver_id=receiver_id, sender_id=sender.id)

            if last_request.status == 'pending':
                raise serializers.ValidationError(
                    {'receiver_id': f'Friend Request has already been sent to {receiver}'}
                )

            if last_request.status == 'rejected' and last_request.last_modified > timezone.now() - timedelta(days=1):
                raise serializers.ValidationError(
                    {'receiver_id': f'{receiver} has rejected your request already. Wait for 24h and try again.'}
                )
            FriendRequest.objects.filter(receiver_id=receiver_id, sender_id=sender.id).delete()
        return validated_data

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver_id', 'status', 'timestamp', 'receiver']


class FriendRequestListSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'sender_id', 'timestamp']


class FriendRequestAccecptRejectSerializer(serializers.ModelSerializer):
    action = serializers.ChoiceField(
        choices=[
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ],
        write_only=True,
        required=True,
        allow_null=False,
    )
    status = serializers.ReadOnlyField()

    def update(self, instance: FriendRequest, validated_data: Dict) -> FriendRequest:
        instance.status = validated_data.get('action', instance.status)
        if validated_data.get('action') == 'accepted':
            instance.sender.add_friend(instance.receiver)

        return super(FriendRequestAccecptRejectSerializer, self).update(instance, validated_data)

    class Meta:
        model = FriendRequest
        fields = ['id', 'status', 'action']
