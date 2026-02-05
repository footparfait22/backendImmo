from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste
    list_display = ('title', 'property_type', 'price', 'city', 'is_published', 'created_at')
    
    # Filtres sur le côté droit
    list_filter = ('property_type', 'is_published', 'city', 'rooms')
    
    # Champs de recherche
    search_fields = ('title', 'description', 'city')
    
    # Organisation du formulaire d'ajout
    fieldsets = (
        ('Informations Générales', {
            'fields': ('title', 'description', 'property_type', 'agent')
        }),
        ('Détails Financiers et Physiques', {
            'fields': ('price', 'surface', 'rooms')
        }),
        ('Localisation', {
            'fields': ('city', 'latitude', 'longitude'),
            'description': "Coordonnées GPS pour la carte de Kinshasa"
        }),
        ('Médias et Statut', {
            'fields': ('image_main', 'is_published')
        }),
    )
    
    
