from django.contrib import admin

from .models import Community, Membership


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "creator",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }



@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "community",
        "joined_at",
    )

    search_fields = (
        "user__username",
        "community__name",
    )