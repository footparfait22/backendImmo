# Core App - ImmoKin

Le module `core` est le point d'entrée principal de l'application Django. Il contient la configuration globale, les routes principales et les fichiers de déploiement.

## 📄 Fichiers Clés

-   **`settings.py`** : Configuration centrale du projet.
    -   Gestion des **variables d'environnement** (`.env`).
    -   Configuration de la **base de données** (dj_database_url).
    -   Configuration de **CORS** (origines autorisées).
    -   Configuration de **Cloudinary** (stockage média).
    -   Configuration de **DRF** (authentification JWT, permissions).
    -   Configuration de **Channels/Redis** (WebSockets).

-   **`urls.py`** : Routeur principal.
    -   Définit les points d'entrée `/admin/`, `/api/`.
    -   Inclut les URLs des autres applications (`properties`, `users`, `visits`, etc.).
    -   Configure les routes d'authentification JWT (`/api/token/`).

-   **`asgi.py`** : Point d'entrée pour le serveur asynchrone (Daphne).
    -   Gère les connexions HTTP et WebSocket via `ProtocolTypeRouter`.
    -   Intègre le middleware d'authentification pour les WebSockets (`AuthMiddlewareStack`).

-   **`wsgi.py`** : Point d'entrée pour le serveur WSGI standard (Gunicorn), utilisé principalement pour servir l'application HTTP classique en production si nécessaire.

## ⚙️ Configuration Spécifique

Ce module utilise `python-dotenv` pour charger les secrets. Assurez-vous que le fichier `.env` à la racine est correctement rempli.

## 🚀 Déploiement

Pour le déploiement (ex: sur Render ou Heroku), le fichier `asgi.py` est crucial car il permet de gérer à la fois le trafic HTTP et WebSocket. Le fichier `Procfile` à la racine du projet pointe généralement vers ce module via `daphne`.
