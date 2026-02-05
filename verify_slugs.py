import os
import django
import sys

# Add project root to path
sys.path.append('/Users/kongoqloo/Desktop/immo_app/backend')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from properties.models import Property

total = Property.objects.count()
empty = Property.objects.filter(slug='').count()
nulls = Property.objects.filter(slug__isnull=True).count()

print(f"Total properties: {total}")
print(f"Properties with empty slug: {empty}")
print(f"Properties with null slug: {nulls}")

if empty == 0 and nulls == 0:
    print("VERIFICATION SUCCESS: All properties have slugs.")
else:
    print("VERIFICATION FAILED: Some properties are missing slugs.")
