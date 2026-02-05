from django.db import models
from django.contrib.auth.models import User
from properties.models import Property  # Import de ton modèle Property

class Conversation(models.Model):
    """
    Représente un fil de discussion entre un client et l'agent 
    pour un bien immobilier spécifique.
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='conversations')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_chats')
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agent_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Empêche de créer plusieurs conversations pour le même binôme sur le même bien
        unique_together = ('property', 'client', 'agent')

    def __str__(self):
        return f"Chat: {self.client.username} -> {self.property.title}"

class Message(models.Model):
    """
    Le contenu individuel de chaque message envoyé.
    """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    visit = models.ForeignKey('visits.Visit', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"De {self.sender.username} le {self.timestamp}"