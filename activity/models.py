import uuid

from django.db import models

from user.models import User


class Action(models.Model):

    REQUEST_SENT = 0
    REQUEST_ACCECPTED = 1
    REQUEST_REJECTED = 2
    USER_BLOCKED = 3
    USER_UNBLOCKED = 4
    MISC_TYPE = 5

    ACTION_TYPES = (
        (REQUEST_SENT, 'Friend Request Sent'),
        (REQUEST_ACCECPTED, 'Friend Request Accepted'),
        (REQUEST_REJECTED, 'Friend Request Rejected'),
        (USER_BLOCKED, 'User Blocked'),
        (USER_UNBLOCKED, 'User unblocked'),
        (MISC_TYPE, 'Misc Type'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    action_type = models.PositiveSmallIntegerField(
        default=MISC_TYPE,
        choices=ACTION_TYPES,
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )
    user = models.ForeignKey(
        'user.User',
        related_name='activity',
        on_delete=models.CASCADE,
    )
    target_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='targeted_activities', null=True, blank=True
    )

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self) -> str:
        return f'#{str(self.id)} - {self.user_id}'
