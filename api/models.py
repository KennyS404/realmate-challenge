import uuid
from django.db import models

class Conversation(models.Model):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    STATE_CHOICES = [
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state = models.CharField(max_length=6, choices=STATE_CHOICES, default=OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} - {self.state}"

class Message(models.Model):
    SENT = 'SENT'
    RECEIVED = 'RECEIVED'
    DIRECTION_CHOICES = [
        (SENT, 'Sent'),
        (RECEIVED, 'Received'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    direction = models.CharField(max_length=8, choices=DIRECTION_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f"Message {self.id} ({self.direction})"
