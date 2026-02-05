from django.core.management.base import BaseCommand
from properties.models import Property
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Génère des slugs uniques pour toutes les propriétés sans slug.'

    def handle(self, *args, **options):
        for prop in Property.objects.all():
            base_slug = slugify(prop.title)
            slug = base_slug
            i = 1
            while Property.objects.filter(slug=slug).exclude(pk=prop.pk).exists():
                slug = f"{base_slug}-{i}"
                i += 1
            prop.slug = slug
            prop.save()
            self.stdout.write(self.style.SUCCESS(f"Propriété {prop.id} : slug généré = {slug}"))
        self.stdout.write(self.style.SUCCESS('Tous les slugs ont été générés !'))
