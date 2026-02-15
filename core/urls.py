from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from properties.views import PropertyViewSet
from users.views import MyTokenObtainPairView, RegisterView, UserDetailView, GoogleLoginView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from chat.views import ConversationViewSet, MessageViewSet

# Router DRF : Génère automatiquement les URLs pour les ViewSets
# Par exemple : /api/properties/, /api/properties/{id}/, etc.
router = routers.DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    # Interface d'administration Django
    path('admin/', admin.site.urls),
    
    # Inclusion des routes de l'API générées par le routeur
    path('api/', include(router.urls)),
    
    # Routes pour les visites (custom)
    path('api/', include('visits.urls')),
    
    # --- Endpoints d'Authentification ---
    # Récupération du token (Login)
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Rafraîchissement du token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Inscription
    path('api/users/register/', RegisterView.as_view(), name='auth_register'),
    # Profil utilisateur courant
    path('api/users/me/', UserDetailView.as_view(), name='auth_me'),
    # Connexion Google (Social Login)
    path('api/token/google/', GoogleLoginView.as_view(), name='google_login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)