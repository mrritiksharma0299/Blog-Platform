from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

from django.http import JsonResponse
from .models import PostLike

from .models import Post, PostLike, Comment
from .forms import PostForm, CommentForm

from django.db.models import Count

from django.contrib.auth.models import User
from django.db.models import Q

from django.utils.crypto import get_random_string
from accounts.models import Follow

from community.models import Membership


from notifications.models import Notification
from accounts.models import Follow


def blog_list(request):

    public_posts = Post.objects.filter(
        published=True,
        visibility="public"
    )


    posts = public_posts


    if request.user.is_authenticated:

        following_users = Follow.objects.filter(
            follower=request.user
        ).values_list(
            "following",
            flat=True
        )


        follower_posts = Post.objects.filter(
            published=True,
            visibility="followers",
            author__in=following_users
        )


        posts = public_posts | follower_posts


    return render(
        request,
        "blog/blog_list.html",
        {
            "posts": posts.order_by("-created_at")
        }
    )


def blog_detail(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug
    )


    # Followers-only blog protection
    if post.visibility == "followers":

        if not request.user.is_authenticated:

            return render(
                request,
                "blog/private_blog.html",
                {
                    "post": post
                }
            )


        is_following = Follow.objects.filter(
            follower=request.user,
            following=post.author
        ).exists()


        if not is_following and request.user != post.author:

            return render(
                request,
                "blog/private_blog.html",
                {
                    "post": post
                }
            )


    # Community blog protection
    if post.visibility == "community":

        if not request.user.is_authenticated:

            return render(
                request,
                "blog/private_blog.html",
                {
                    "post": post
                }
            )


        is_member = Membership.objects.filter(
            user=request.user,
            community=post.community
        ).exists()


        if not is_member and request.user != post.author:

            return render(
                request,
                "blog/private_blog.html",
                {
                    "post": post
                }
            )



    comments = post.comments.all()


    liked = False


    if request.user.is_authenticated:

        liked = PostLike.objects.filter(
            user=request.user,
            post=post
        ).exists()



    if request.method == "POST":

        if request.user.is_authenticated:

            form = CommentForm(request.POST)


            if form.is_valid():

                comment = form.save(commit=False)

                comment.user = request.user

                comment.post = post

                comment.save()

                if post.author != request.user:

                    Notification.objects.create(

                        sender=request.user,

                        receiver=post.author,

                        notification_type="comment",

                        message=f"{request.user.username} commented on your blog.",

                        post=post

                    )

                return redirect(
                    post.get_absolute_url()
                )


    else:

        form = CommentForm()



    return render(
        request,
        "blog/blog_detail.html",
        {
            "post": post,
            "liked": liked,
            "comments": comments,
            "form": form,
        },
    )
@login_required
def create_blog(request):

    if request.method == "POST":

        print(request.POST)

        form = PostForm(
            request.POST,
            request.FILES,
            user=request.user
        )

        if form.is_valid():

            print("FORM VALID")

            post = form.save(commit=False)

            post.author = request.user

            if form.cleaned_data["category"] == "Other":
                post.category = form.cleaned_data["other_category"].title()
            else:
                post.category = form.cleaned_data["category"]

            visibility = form.cleaned_data["visibility"]

            post.visibility = visibility

            if visibility == "community":
                post.community = form.cleaned_data["community"]

            print("Saving post...")

            post.save()

            print("Post saved!")

            followers = Follow.objects.filter(
                following=request.user
            )

            print("Followers:", followers.count())

            for follow in followers:

                print("Creating notification for", follow.follower)

                Notification.objects.create(
                    sender=request.user,
                    receiver=follow.follower,
                    notification_type="blog",
                    message=f"{request.user.username} posted a new blog.",
                    post=post
                )

            print("Finished")

            return redirect("blog_list")

        else:

            print("FORM INVALID")
            print(form.errors)

    else:

        form = PostForm(user=request.user)

    return render(
        request,
        "blog/create_blog.html",
        {"form": form}
    )


@login_required
def toggle_like(request, slug):

    post = get_object_or_404(Post, slug=slug)

    like = PostLike.objects.filter(
        user=request.user,
        post=post
    )

    if like.exists():

        like.delete()

        liked = False

    else:

        PostLike.objects.create(
            user=request.user,
            post=post
        )

        liked = True

        if post.author != request.user:

            Notification.objects.create(

                sender=request.user,

                receiver=post.author,

                notification_type="like",

                message=f"{request.user.username} liked your blog.",

                post=post

            )

    return JsonResponse({

        "liked": liked,

        "total_likes": post.total_likes,

    })


@login_required
def delete_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id,
        user=request.user
    )

    post = comment.post

    comment.delete()

    return redirect(post.get_absolute_url())


@login_required
def edit_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id,
        user=request.user
    )

    if request.method == "POST":

        form = CommentForm(
            request.POST,
            instance=comment
        )

        if form.is_valid():

            form.save()

            return redirect(comment.post.get_absolute_url())

    else:

        form = CommentForm(instance=comment)

    return render(
        request,
        "blog/edit_comment.html",
        {
            "form": form,
            "comment": comment,
        },
    )



def category_list(request):

    posts = Post.objects.filter(
        published=True,
        visibility="public"
    )


    if request.user.is_authenticated:

        following_users = Follow.objects.filter(
            follower=request.user
        ).values_list(
            "following",
            flat=True
        )


        follower_posts = Post.objects.filter(
            published=True,
            visibility="followers",
            author__in=following_users
        )


        posts = posts | follower_posts



    categories = (
        posts
        .values("category")
        .annotate(total=Count("id"))
        .order_by("category")
    )


    return render(
        request,
        "blog/category_list.html",
        {
            "categories": categories,
        },
    )

def category_detail(request, category):

    public_posts = Post.objects.filter(
        published=True,
        visibility="public",
        category__iexact=category,
    )


    posts = public_posts


    if request.user.is_authenticated:

        following_users = Follow.objects.filter(
            follower=request.user
        ).values_list(
            "following",
            flat=True
        )


        follower_posts = Post.objects.filter(
            published=True,
            visibility="followers",
            category__iexact=category,
            author__in=following_users
        )


        posts = public_posts | follower_posts



    return render(
        request,
        "blog/category_detail.html",
        {
            "posts": posts.order_by("-created_at"),
            "category": category,
        },
    )
@login_required
def delete_blog(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug,
        author=request.user,
    )

    if request.method == "POST":
        post.delete()
        return redirect("profile")

    return render(
        request,
        "blog/delete_blog.html",
        {
            "post": post
        }
    )

def search(request):

    query = request.GET.get("q", "").strip()

    users = User.objects.none()
    posts = Post.objects.none()
    categories = []


    if query:

        users = User.objects.filter(
            username__icontains=query
        )


        public_posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__icontains=query) |
            Q(country__icontains=query),
            published=True,
            visibility="public",
        )


        posts = public_posts


        if request.user.is_authenticated:

            following_users = Follow.objects.filter(
                follower=request.user
            ).values_list(
                "following",
                flat=True
            )


            follower_posts = Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(category__icontains=query) |
                Q(country__icontains=query),
                published=True,
                visibility="followers",
                author__in=following_users,
            )


            posts = public_posts | follower_posts



        categories = (
            posts
            .values_list(
                "category",
                flat=True
            )
            .distinct()
        )


    return render(
        request,
        "blog/search.html",
        {
            "query": query,
            "users": users,
            "posts": posts,
            "categories": categories,
        },
    )