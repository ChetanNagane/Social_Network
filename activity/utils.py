from activity.models import Action


class ActionType:
    """
    Helper class to define the different types of actions.
    """

    REQUEST_SENT = 0
    REQUEST_ACCECPTED = 1
    REQUEST_REJECTED = 2
    USER_BLOCKED = 3
    USER_UNBLOCKED = 4
    MISC_TYPE = 5


def create_action(
    user,
    target_user,
    action_type: int = Action.MISC_TYPE,
) -> Action:
    """
    Create an action for the given user with the given content.
    """
    return Action.objects.create(user=user, target_user=target_user, action_type=action_type)
