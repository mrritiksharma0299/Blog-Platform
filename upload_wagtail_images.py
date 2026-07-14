import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "mysite.settings.dev"
)

django.setup()

from django.core.files import File
from wagtail.images import get_image_model


Image = get_image_model()


image_folder = "media/original_images"


for filename in os.listdir(image_folder):

    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):

        file_path = os.path.join(image_folder, filename)

        with open(file_path, "rb") as f:

            image = Image.objects.create(
                title=os.path.splitext(filename)[0],
                file=File(f, name=filename)
            )

            print("✅ Uploaded:", image.title)


print("\nFinished uploading images!")