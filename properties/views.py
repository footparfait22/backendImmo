from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Property, PropertyImage
from .serializers import PropertySerializer
from .permissions import IsOwnerOrAdmin

class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [IsOwnerOrAdmin]
    lookup_field = 'slug'
    filterset_fields = ['property_type', 'listing_type', 'city', 'commune']
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and (user.is_staff or user.is_superuser):
            return Property.objects.all().order_by('-created_at')
        return Property.objects.filter(is_published=True).order_by('-created_at')

    def perform_create(self, serializer):
        # Save the property first, setting the agent
        property_instance = serializer.save(agent=self.request.user)
        
        # Handle multiple images upload
        images = self.request.FILES.getlist('images')
        for image in images:
            PropertyImage.objects.create(property=property_instance, image=image)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def toggle_favorite(self, request, slug=None):
        property_obj = self.get_object()
        user = request.user
        if property_obj.favorites.filter(id=user.id).exists():
            property_obj.favorites.remove(user)
            return Response({'status': 'removed', 'likes_count': property_obj.favorites.count()})
        else:
            property_obj.favorites.add(user)
            return Response({'status': 'added', 'likes_count': property_obj.favorites.count()})

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def favorites(self, request):
        favorites = request.user.favorite_properties.all()
        serializer = self.get_serializer(favorites, many=True)
        return Response(serializer.data)