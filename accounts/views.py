from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm, UserUpdateForm
from .models import Profile

from django.shortcuts import get_object_or_404,  redirect

from .models import Profile, Follow

from blog.models import Post
from django.views.decorators.http import require_POST
from django.contrib import messages

from community.models import Community, Membership
from .models import Follow

from notifications.models import Notification

def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("login")

    else:
        form = RegisterForm()


    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("home")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("/")



@login_required
def profile_view(request):

    posts = Post.objects.filter(
        author=request.user
    ).order_by("-created_at")

    context = {
        "posts": posts,

        "total_blogs": posts.count(),

        "public_blogs": posts.filter(
            visibility="public"
        ).count(),

        "followers_blogs": posts.filter(
            visibility="followers"
        ).count(),

        "community_blogs": posts.filter(
            visibility="community"
        ).count(),

        "followers_count": Follow.objects.filter(
            following=request.user
        ).count(),

        "following_count": Follow.objects.filter(
            follower=request.user
        ).count(),

        "communities_count": Membership.objects.filter(
            user=request.user
        ).count(),

        "communities": Community.objects.filter(
            members__user=request.user
        ),
    }

    return render(
        request,
        "accounts/profile.html",
        context,
    )



@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()

            return redirect("profile")

    else:

        user_form = UserUpdateForm(
            instance=request.user
        )

        profile_form = ProfileForm(
            instance=profile
        )


    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(
        request,
        "accounts/edit_profile.html",
        context
    )


def public_profile(request, username):

    profile_user = get_object_or_404(
        User,
        username=username
    )


    is_following = False
    follows_you = False


    if request.user.is_authenticated:

        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user,
        ).exists()

        follows_you = Follow.objects.filter(
            follower=profile_user,
            following=request.user,
        ).exists()



    posts = Post.objects.filter(
        author=profile_user
    ).order_by("-created_at")



    public_blogs = Post.objects.filter(
        author=profile_user,
        visibility="public"
    ).order_by("-created_at")


    private_blogs = Post.objects.none()

    if is_following:
        private_blogs = Post.objects.filter(
            author=profile_user,
            visibility="followers"
        ).order_by("-created_at")




    communities = Community.objects.filter(
        members__user=profile_user
    )



    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()



    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()



    return render(
        request,
        "accounts/public_profile.html",
        {
            "profile_user": profile_user,

            "is_following": is_following,

            "follows_you": follows_you,

            "followers_count": followers_count,

            "following_count": following_count,

            "total_blogs": public_blogs.count(),

            "public_blogs": public_blogs,

            "private_blogs": private_blogs,

            "communities": communities,

            "communities_count": communities.count(),

        }
    )


@login_required
def toggle_follow(request, username):

    target_user = get_object_or_404(
        User,
        username=username
    )


    if target_user == request.user:

        return redirect(
            "public_profile",
            username=username
        )


    follow = Follow.objects.filter(
        follower=request.user,
        following=target_user
    )


    if follow.exists():

        follow.delete()


    else:

        Follow.objects.create(
            follower=request.user,
            following=target_user
        )


        Notification.objects.create(

            receiver=target_user,

            sender=request.user,

            notification_type="follow",

            message=f"{request.user.username} started following you"

        )


    return redirect(
        "public_profile",
        username=username
    )

def followers_list(request, username):

    profile_user = get_object_or_404(
        User,
        username=username
    )

    followers = [
        follow.follower
        for follow in profile_user.followers.all()
    ]

    return render(
        request,
        "accounts/followers.html",
        {
            "profile_user": profile_user,
            "followers": followers,
        },
    )


def following_list(request, username):

    profile_user = get_object_or_404(
        User,
        username=username
    )

    following = [
        follow.following
        for follow in profile_user.following.all()
    ]

    return render(
        request,
        "accounts/following.html",
        {
            "profile_user": profile_user,
            "following": following,
        },
    )


@login_required
@require_POST
def delete_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user
    )

    post.delete()

    return redirect("profile")


@login_required
def delete_blog(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug,
        author=request.user
    )

    if request.method == "POST":
        post.delete()
        messages.success(request, "Blog deleted successfully.")
        return redirect("profile")

    return render(
        request,
        "blog/delete_blog.html",
        {
            "post": post,
        },
    )