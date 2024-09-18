import random

from django.core.management.base import BaseCommand
from django.db import connection

from user.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        user_ids = list(User.objects.only('id').values_list('id', flat=True))

        random.shuffle(user_ids)
        batch1 = user_ids[0:10000]
        random.shuffle(user_ids)
        batch2 = user_ids[0:10000]

        pairs = []
        for u1, u2 in zip(batch1, batch2):
            pairs.append(f'({u1}, {u2})')
            pairs.append(f'({u2}, {u1})')

        pairs = ",".join(pairs)
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
            INSERT INTO user_user_friends (from_user_id, to_user_id)
            VALUES {pairs}
            ON CONFLICT DO NOTHING;"""
            )
