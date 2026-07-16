import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.production")
django.setup()

from blog.models import Post
import cloudinary.uploader
import cloudinary.api


for post in Post.objects.all():

    img = post.featured_image

    if not img:
        continue

    try:
        cloudinary.api.resource(img.public_id)
        print("OK:", post.title)

    except Exception:

        print("Missing:", post.title, img.public_id)

        filename = img.public_id.split("/")[-1]

        local_path = f"media/blog_images/{filename}.jpg"

        if os.path.exists(local_path):

            result = cloudinary.uploader.upload(
                local_path,
                public_id=img.public_id,
                overwrite=True
            )

            post.featured_image = result["public_id"]
            post.save()

            print("Uploaded:", result["public_id"])

        else:
            print("Not found:", local_path)