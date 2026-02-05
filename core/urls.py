from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from properties.views import PropertyViewSet
from users.views import MyTokenObtainPairView, RegisterView, UserDetailView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from chat.views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('visits.urls')),
    
    # Auth Endpoints
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/register/', RegisterView.as_view(), name='auth_register'),
    path('api/users/me/', UserDetailView.as_view(), name='auth_me'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)