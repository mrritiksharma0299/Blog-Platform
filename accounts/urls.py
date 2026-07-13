from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from django.urls import path
from .views import profile_view

from django.urls import include

urlpatterns = [

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html"
        ),
        name="login",
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),

    path(
        "register/",
        views.register_view,
        name="register",
    ),

    path(
        "profile/",
        profile_view, 
        name="profile"
        ), 

    path(
        "edit-profile/",
        views.edit_profile,
        name="edit_profile"
    ),
    
    path(
        "<str:username>/followers/",
        views.followers_list,
        name="followers_list",
    ),

    path(
        "<str:username>/following/",
        views.following_list,
        name="following_list",
    ),

    path(
        "user/<str:username>/",
        views.public_profile,
        name="public_profile"
    ),
    path(
        "follow/<str:username>/",
        views.toggle_follow,
        name="toggle_follow",
    ),
    
]