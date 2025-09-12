from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='topics_created'
    )
    partitions = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TopicRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
    ]
    topic_name = models.CharField(max_length=255)
    partitions = models.PositiveIntegerField(default=1)
    requested_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='topic_requests'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    reviewed_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='reviewed_topic_requests'
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.topic_name} ({self.status})"

class LoginEntry(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='login_entries'
    )
    success = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {'Success' if self.success else 'Failed'}"