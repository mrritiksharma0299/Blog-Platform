import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.dev")

import django
django.setup()

from django.core.files import File
from blog.models import Post

for post in Post.objects.all():
    if not post.featured_image:
        continue

    filename = os.path.basename(post.featured_image.name)
    local_path = os.path.join("media", "blog_images", filename)

    print(f"\nProcessing: {post.title}")
    print(f"Looking for: {local_path}")

    if os.path.exists(local_path):
        with open(local_path, "rb") as f:
            post.featured_image.save(filename, File(f), save=True)
        print("✅ Uploaded successfully")
    else:
        print("❌ File not found:", local_path)

print("\nFinished!")