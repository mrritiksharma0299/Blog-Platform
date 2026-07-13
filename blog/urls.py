from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.blog_list,
        name="blog_list"
    ),

    path(
        "create/",
        views.create_blog,
        name="create_blog"
    ),


    path(
        "categories/",
        views.category_list,
        name="category_list",
    ),

    path(
        "category/<str:category>/",
        views.category_detail,
        name="category_detail",
    ),

    path(
        "search/",
        views.search,
        name="search",
    ),

    path(
        "<slug:slug>/",
        views.blog_detail,
        name="blog_detail"
    ),

    path(
        "<slug:slug>/like/",
        views.toggle_like,
        name="toggle_like",
    ),
    
    path(
        "comment/<int:comment_id>/delete/",
        views.delete_comment,
        name="delete_comment",
    ),

    path(
        "comment/<int:comment_id>/edit/",
        views.edit_comment,
        name="edit_comment",
    ),

    path(
        "delete/<slug:slug>/",
        views.delete_blog,
        name="delete_blog",
    ),

    path(
        "delete/<slug:slug>/",
        views.delete_blog,
        name="delete_blog",
    ),
]