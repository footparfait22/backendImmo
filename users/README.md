# Users App - ImmoKin

L'application `users` gère l'authentification, les profils utilisateurs et les rôles au sein de la plateforme.

## 📦 Modèles (`models.py`)

-   **`Profile`** : Extension du modèle `User` standard de Django.
    -   **`user`** : Lien OneToOne vers le modèle `User`.
    -   **`role`** : Type d'utilisateur (`client` ou `agent`).
    -   **`phone`** : Numéro de téléphone.
    -   **`avatar`** : Image de profil.

Un signal `post_save` crée automatiquement un `Profile` vide lors de la création d'un `User`.

## 🔒 Authentification & Sécurité

-   **JWT (JSON Web Tokens)** : L'authentification principale repose sur `simplejwt`.
-   **Google OAuth** : Support de l'authentification via Google Sign-In.
    -   Le token Google est vérifié côté backend via l'endpoint `/api/token/google/`.
    -   Si l'email est valide, un utilisateur Django est créé ou récupéré, et une paire de tokens JWT est renvoyée.

## 🛠️ Vues (`views.py`)

-   **`RegisterView`** : Inscription d'un nouvel utilisateur (avec rôle).
-   **`MyTokenObtainPairView`** : Connexion classique (Username/Password). Renvoie le rôle et l'avatar dans la réponse.
-   **`GoogleLoginView`** : Gestion du login Google.
-   **`UserDetailView`** : Récupération et mise à jour du profil de l'utilisateur connecté (`/users/me/`).

## 📝 Serializers (`serializers.py`)

-   **`UserSerializer`** : Sérialisation complète de l'utilisateur avec son profil imbriqué.
-   **`RegisterSerializer`** : Validation des données d'inscription.
-   **`MyTokenObtainPairSerializer`** : Personnalisation du payload JWT pour inclure le `role` et le `username` directement dans le token décodé.
