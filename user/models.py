from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    friends = models.ManyToManyField('User', blank=True)

    def __str__(self):
        return self.username

    def add_friend(self, friend):
        self.friends.add(friend)
        friend.friends.add(self)


class BlockUser(models.Model):
    blocker = models.ForeignKey("user.User", related_name='blocked_by', on_delete=models.CASCADE)
    blocked = models.ForeignKey("user.User", related_name='blocked', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['blocker', 'blocked']
