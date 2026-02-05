import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile

users = User.objects.all()
count = 0
for user in users:
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user, role='admin' if user.is_superuser else 'client')
        print(f"Created profile for {user.username}")
        count += 1
    else:
        print(f"Profile exists for {user.username}")

print(f"Done. Created {count} missing profiles.")
