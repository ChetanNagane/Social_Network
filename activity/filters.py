from django_filters import rest_framework as filters

from activity.models import Action
from user.models import User


class ActionFilter(filters.FilterSet):
    user = filters.ModelMultipleChoiceFilter(queryset=User.objects.only('username'))

    class Meta:
        model = Action
        fields = {
            'timestamp': ['gte', 'lte', 'date__gte', 'date__lte', 'date__lt'],
        }
