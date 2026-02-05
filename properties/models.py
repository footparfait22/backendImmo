from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Property(models.Model):
    
    TYPES = (
        ('Maison', 'Maison'),
        ('apartment', 'Appartement'),
        ('Terrain', 'Terrain'),
        ('commercial', 'Commercial'),
    )
    LISTING_TYPES = (
        ('Vente', 'Vente'),
        ('Location', 'Location'),
    )



    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=TYPES)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPES, default='Location')
    
    price = models.DecimalField(max_digits=12, decimal_places=2)
    surface = models.IntegerField(help_text="Surface en m²", null=True, blank=True)
    rooms = models.IntegerField(null=True, blank=True)
    
    # Adresse détaillée
    city = models.CharField(max_length=100, default="Kinshasa")
    commune = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100, blank=True, verbose_name="Quartier")
    avenue = models.CharField(max_length=100, blank=True)
    street_number = models.CharField(max_length=20, blank=True, verbose_name="Numéro")

    # Géolocalisation
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    image_main = models.ImageField(upload_to='properties/%Y/%m/%d/')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    favorites = models.ManyToManyField(User, related_name='favorite_properties', blank=True)
    
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/gallery/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"