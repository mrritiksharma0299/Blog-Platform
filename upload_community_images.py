import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.dev")

import django
django.setup()

from django.core.files import File
from community.models import Community

for community in Community.objects.all():

    if not community.image:
        continue

    filename = os.path.basename(community.image.name)
    local_path = os.path.join("media", "community", filename)

    print(f"\nCommunity: {community.name}")
    print(f"Looking for: {local_path}")

    if os.path.exists(local_path):
        with open(local_path, "rb") as f:
            community.image.save(filename, File(f), save=True)
        print("✅ Uploaded")
    else:
        print("❌ File not found")

print("\nFinished!")