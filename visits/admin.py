from django.contrib import admin
from .models import Visit

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste
    list_display = ('id', 'property_title', 'client_name', 'proposed_date', 'status', 'created_at')
    
    # Filtres latéraux pour trier rapidement
    list_filter = ('status', 'proposed_date', 'created_at')
    
    # Barre de recherche (recherche par titre du bien ou nom du client)
    search_fields = ('property__title', 'conversation__client__username', 'conversation__agent__username')
    
    # Rendre certaines colonnes cliquables pour éditer
    list_editable = ('status',)
    
    # Organisation du formulaire d'édition
    fieldsets = (
        ('Informations Générales', {
            'fields': ('conversation', 'property', 'status')
        }),
        ('Planification', {
            'fields': ('proposed_date',),
            'description': 'Choisissez la date et l\'heure de la visite.'
        }),
    )

    def property_title(self, obj):
        return obj.property.title
    property_title.short_description = 'Bien Immobilier'

    def client_name(self, obj):
        return obj.conversation.client.username
    client_name.short_description = 'Client'

    # Optionnel : permettre de voir la visite directement dans le calendrier admin
    date_hierarchy = 'proposed_date'