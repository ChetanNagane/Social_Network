from rest_framework import serializers

from activity.models import Action
from user.models import User


class SmallUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
        )


class ActionSerializer(serializers.ModelSerializer):
    user = SmallUserSerializer(read_only=True)
    target_user = SmallUserSerializer(read_only=True)
    action_type = serializers.CharField(source='get_action_type_display', read_only=True)

    only_fields = ('id', 'timestamp', 'action_type') + tuple(
        f'user__{field}' for field in SmallUserSerializer.Meta.fields
    )

    class Meta:
        model = Action
        fields = ('id', 'timestamp', 'user', 'target_user', 'action_type')
