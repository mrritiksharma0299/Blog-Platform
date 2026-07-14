import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.dev")

import django
django.setup()

from django.core.files import File
from accounts.models import Profile

for profile in Profile.objects.all():

    if not profile.profile_image:
        continue

    filename = os.path.basename(profile.profile_image.name)
    local_path = os.path.join("media", "profiles", filename)

    print(f"\nUser: {profile.user.username}")
    print(f"Looking for: {local_path}")

    if os.path.exists(local_path):
        with open(local_path, "rb") as f:
            profile.profile_image.save(filename, File(f), save=True)
        print("✅ Uploaded")
    else:
        print("❌ File not found")

print("\nFinished!")