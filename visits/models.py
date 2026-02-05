from django.db import models
from django.contrib.auth.models import User
from properties.models import Property
from chat.models import Conversation

class Visit(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('ACCEPTED', 'Acceptée'),
        ('DECLINED', 'Refusée'),
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='visits')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    proposed_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visite {self.property.title} - {self.proposed_date}"