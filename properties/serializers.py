from rest_framework import serializers
from .models import Property, PropertyImage

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'created_at']

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    agent = serializers.StringRelatedField(read_only=True)
    agent_id = serializers.ReadOnlyField(source='agent.id')
    likes_count = serializers.IntegerField(source='favorites.count', read_only=True)
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['agent', 'created_at', 'images', 'favorites']

    def get_is_favorite(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.favorites.filter(id=user.id).exists()
        return False