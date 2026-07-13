from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.community_list,
        name="community_list"
    ),

    path(
        "create/",
        views.create_community,
        name="create_community"
    ),

    path(
        "<slug:slug>/chat/",
        views.community_chat,
        name="community_chat",
    ),

    path(
        "<slug:slug>/",
        views.community_detail,
        name="community_detail"
    ),

    path(
        "<slug:slug>/join/",
        views.toggle_membership,
        name="toggle_membership"
    ),

    path(
        "<slug:slug>/chat/",
        views.community_chat,
        name="community_chat"
    ),
    path(
        "<slug:slug>/feed/",
        views.community_feed,
        name="community_feed",
    ),
]