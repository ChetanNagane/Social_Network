import csv
import uuid
from concurrent.futures import ThreadPoolExecutor

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from user.models import User

BATCH_SIZE = 1000
NUM_THREADS = 10


def insert_users(batch):

    users = []
    for row in batch:
        user = User(
            email=row['email'],
            username=f'{row["username"]}{str(uuid.uuid4())[:4]}',
            first_name=row['first_name'],
            last_name=row['last_name'],
            password=make_password(row['password'], None, 'md5'),  # using weak hasher to speed up
        )
        users.append(user)

    User.objects.bulk_create(users, batch_size=BATCH_SIZE)
    print('.', end='', flush=True)


class Command(BaseCommand):
    help = "Load sample data from CSV into the User model using multithreading"

    def add_users(self):
        with open('sample_users.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            batch = []
            batches = []

            for row in reader:
                batch.append(row)
                if len(batch) >= BATCH_SIZE:
                    batches.append(batch)
                    batch = []

            if batch:
                batches.append(batch)

            with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
                executor.map(insert_users, batches)

            self.stdout.write(self.style.SUCCESS("Successfully added sample user data."))

    def handle(self, *args, **kwargs):
        self.add_users()
