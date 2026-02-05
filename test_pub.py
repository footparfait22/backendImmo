import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from properties.models import Property

def test_publication():
    # Setup
    admin_user, _ = User.objects.get_or_create(username='test_admin', is_staff=True)
    regular_user, _ = User.objects.get_or_create(username='test_user', is_staff=False)
    
    # Simulate perform_create logic
    def create_prop(user, title):
        is_published = user.is_staff or user.is_superuser
        p = Property.objects.create(
            title=title,
            agent=user,
            is_published=is_published,
            price=1000,
            commune='Test',
            image_main='test.jpg'
        )
        return p

    p1 = create_prop(admin_user, "Admin Prop")
    p2 = create_prop(regular_user, "User Prop")

    print(f"Admin Prop: is_published={p1.is_published}")
    print(f"User Prop: is_published={p2.is_published}")

    # Cleanup
    p1.delete()
    p2.delete()

if __name__ == "__main__":
    test_publication()
