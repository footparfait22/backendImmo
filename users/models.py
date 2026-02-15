from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """
    Extension du modèle User standard de Django.
    Permet de stocker des informations supplémentaires comme le rôle (Client/Agent), 
    le numéro de téléphone et l'avatar.
    Lie chaque utilisateur à un profil unique (OneToOne).
    """
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('agent', 'Agent'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# Signal : Automatisation
# À chaque fois qu'un User est créé (post_save), cette fonction est déclenchée 
# pour créer automatiquement le Profile associé vide.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)