from rest_framework import serializers
from .models import Conversation, Message
from visits.models import Visit
from visits.serializers import VisitSerializer

class VisitShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ['id', 'proposed_date', 'status']

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.ReadOnlyField(source='sender.username')
    visit = VisitSerializer(read_only=True) # On embarque l'objet visite

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'sender_name', 'text', 'timestamp', 'is_read', 'visit']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    property_title = serializers.ReadOnlyField(source='property.title')
    property_slug = serializers.ReadOnlyField(source='property.slug')
    property_image = serializers.SerializerMethodField()
    client_username = serializers.ReadOnlyField(source='client.username')
    client_avatar = serializers.SerializerMethodField()
    agent_username = serializers.ReadOnlyField(source='agent.username')
    agent_avatar = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'property', 'property_title', 'property_slug', 'property_image',
            'client', 'client_username', 'client_avatar',
            'agent', 'agent_username', 'agent_avatar',
            'messages', 'last_message', 'unread_count', 'created_at', 'updated_at'
        ]

    def get_client_avatar(self, obj):
        if hasattr(obj.client, 'profile') and obj.client.profile.avatar:
            return obj.client.profile.avatar.url
        return None

    def get_agent_avatar(self, obj):
        if hasattr(obj.agent, 'profile') and obj.agent.profile.avatar:
            return obj.agent.profile.avatar.url
        return None

    def get_unread_count(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.messages.filter(is_read=False).exclude(sender=user).count()
        return 0

    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return {
                'text': last_msg.text,
                'timestamp': last_msg.timestamp,
                'sender_name': last_msg.sender.username
            }
        return None

    def get_property_image(self, obj):
        if obj.property.image_main:
            return obj.property.image_main.url
        return None