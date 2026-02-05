from rest_framework import serializers
from .models import Visit

class VisitSerializer(serializers.ModelSerializer):
    property_title = serializers.ReadOnlyField(source='property.title')
    property_slug = serializers.ReadOnlyField(source='property.slug')

    class Meta:
        model = Visit
        fields = ['id', 'conversation', 'property', 'property_title', 'property_slug', 'proposed_date', 'status', 'created_at']
        read_only_fields = []