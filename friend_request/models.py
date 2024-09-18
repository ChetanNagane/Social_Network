from django.db import models


class FriendRequest(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    sender = models.ForeignKey("user.User", related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey("user.User", related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.status})"

    class Meta:
        unique_together = ['sender', 'receiver']
