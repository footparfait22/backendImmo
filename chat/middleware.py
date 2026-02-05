import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.db import close_old_connections

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # On ferme les anciennes connexions pour éviter les fuites de mémoire
        close_old_connections()
        
        # Récupérer le token depuis l'URL (ex: ws://.../?token=ABC)
        query_string = scope.get("query_string", b"").decode("utf-8")
        query_params = dict(qc.split("=") for qc in query_string.split("&") if "=" in qc)
        token = query_params.get("token")

        if token:
            try:
                # On décode le JWT avec la SECRET_KEY de Django
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                scope["user"] = await get_user(decoded_data["user_id"])
            except (jwt.ExpiredSignatureError, jwt.DecodeError, KeyError):
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)