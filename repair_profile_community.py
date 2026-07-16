import os
import django

import glob

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "mysite.settings.production"
)

django.setup()

import cloudinary.api
import cloudinary.uploader

from accounts.models import Profile
from community.models import Community


def repair_image(obj, field, folder):

    image = getattr(obj, field)

    if not image:
        return

    public_id = str(image)

    try:
        cloudinary.api.resource(public_id)
        print("OK:", public_id)

    except Exception:

        print("Missing:", public_id)

        filename = public_id.split("/")[-1]

        parts = filename.rsplit("_", 1)

        if len(parts) == 2:
            filename_without_suffix = parts[0]
        else:
            filename_without_suffix = filename

        extensions = [
            ".jpg",
            ".png",
            ".jpeg"
        ]

        local_file = None

        for name in [filename, filename_without_suffix]:
            for ext in extensions:
                path = f"media/{folder}/{name}{ext}"
                if os.path.exists(path):
                    local_file = path
                    break
            if local_file:
                break

        if local_file:

            result = cloudinary.uploader.upload(
                local_file,
                public_id=public_id,
                overwrite=True
            )

            setattr(
                obj,
                field,
                result["public_id"]
            )

            obj.save()

            print(
                "Uploaded:",
                result["public_id"]
            )

        else:
            print(
                "LOCAL FILE NOT FOUND:",
                filename
            )


print("\n--- PROFILE IMAGES ---")

for profile in Profile.objects.all():
    repair_image(
        profile,
        "profile_image",
        "profiles"
    )


print("\n--- COMMUNITY IMAGES ---")


print("\nFiles in media/community:")


for f in glob.glob("media/community/*"):
    print(f)

for community in Community.objects.all():
    repair_image(
        community,
        "image",
        "community"
    )