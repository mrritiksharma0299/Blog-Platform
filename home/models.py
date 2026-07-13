from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.images.models import Image

from blog.models import Post


class HomePage(Page):

    hero_title = models.CharField(
        max_length=200,
        default="Discover Stories From Around The World"
    )

    hero_description = RichTextField(
        blank=True
    )

    hero_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )


    content_panels = Page.content_panels + [

        FieldPanel("hero_title"),
        FieldPanel("hero_description"),
        FieldPanel("hero_image"),

    ]


    def get_context(self, request):

        context = super().get_context(request)


        context["trending_posts"] = Post.objects.filter(
            published=True
        ).order_by("-created_at")[:6]


        return context