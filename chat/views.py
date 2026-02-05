from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Un utilisateur ne voit que ses conversations (soit client, soit agent)
        user = self.request.user
        queryset = Conversation.objects.filter(Q(client=user) | Q(agent=user))
        
        property_id = self.request.query_params.get('property')
        if property_id:
            queryset = queryset.filter(property_id=property_id)
            
        return queryset.order_by('-updated_at')

    @action(detail=False, methods=['get'])
    def total_unread_count(self, request):
        user = request.user
        unread_count = Message.objects.filter(
            conversation__in=Conversation.objects.filter(Q(client=user) | Q(agent=user)),
            is_read=False
        ).exclude(sender=user).count()
        return Response({'unread_count': unread_count})

    def perform_create(self, serializer):
        # Optionnel: logique auto pour l'agent ou le client
        serializer.save()

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # On filtre par conversation_id passé en paramètre
        conversation_id = self.request.query_params.get('conversation')
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')
        return Message.objects.none()
