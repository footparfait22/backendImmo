from rest_framework import viewsets, permissions
from .models import Visit
from .serializers import VisitSerializer

class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # On peut ajouter de la logique ici (ex: vérifier que l'user est l'agent)
        serializer.save()