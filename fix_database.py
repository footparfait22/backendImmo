import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def fix():
    with connection.cursor() as cursor:
        print("Checking for slug column in properties_property...")
        
        # Add slug column if it doesn't exist
        try:
            cursor.execute("ALTER TABLE properties_property ADD COLUMN IF NOT EXISTS slug VARCHAR(255);")
            print("Column 'slug' added or already exists.")
        except Exception as e:
            print(f"Error adding column: {e}")

        # Try to make it unique and add index, ignoring if already exists
        try:
            # First, fill empty slugs to avoid unique constraint violation
            from properties.models import Property
            from django.utils.text import slugify
            
            for prop in Property.objects.filter(slug__isnull=True) | Property.objects.filter(slug=''):
                base_slug = slugify(prop.title) or 'property'
                slug = base_slug
                counter = 1
                while Property.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                prop.slug = slug
                prop.save()
            print("Slugs populated.")

            # Now try to set UNIQUE constraint
            # We don't use 'IF NOT EXISTS' for UNIQUE constraints easily in raw SQL without more logic, 
            # but we can wrap it in a try/except.
            try:
                cursor.execute("ALTER TABLE properties_property ADD CONSTRAINT properties_property_slug_unique UNIQUE (slug);")
                print("Unique constraint added.")
            except Exception as e:
                print(f"Constraint might already exist: {e}")

        except Exception as e:
            print(f"General error during data fix: {e}")

if __name__ == "__main__":
    fix()
