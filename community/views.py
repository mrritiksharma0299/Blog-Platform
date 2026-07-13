from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Community

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import CommunityForm, CommunityMessageForm

from .models import Community, Membership, CommunityMessage

from blog.models import Post

def community_list(request):

    communities = Community.objects.all()

    return render(
        request,
        "community/community_list.html",
        {
            "communities": communities
        }
    )


@login_required
def create_community(request):

    if request.method == "POST":

        form = CommunityForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            community = form.save(commit=False)

            community.creator = request.user

            community.save()

            return redirect(
                "community_detail",
                slug=community.slug
            )

    else:

        form = CommunityForm()

    return render(
        request,
        "community/create_community.html",
        {
            "form": form
        }
    )


def community_detail(request, slug):

    community = get_object_or_404(
        Community,
        slug=slug
    )

    community_posts = Post.objects.filter(
        community=community,
        published=True
    ).order_by("-created_at")

    is_member = False

    if request.user.is_authenticated:

        is_member = Membership.objects.filter(
            user=request.user,
            community=community
        ).exists()

    context = {
        "community": community,
        "is_member": is_member,
        "community_posts": community_posts,
    }

    return render(
        request,
        "community/community_detail.html",
        context
    )

@login_required
def toggle_membership(request, slug):

    community = get_object_or_404(
        Community,
        slug=slug
    )

    membership = Membership.objects.filter(
        user=request.user,
        community=community
    )

    if membership.exists():

        membership.delete()

    else:

        Membership.objects.create(
            user=request.user,
            community=community
        )

    return redirect(
        "community_detail",
        slug=community.slug
    )

@login_required
def community_chat(request, slug):

    community = get_object_or_404(
        Community,
        slug=slug
    )

    is_member = Membership.objects.filter(
        user=request.user,
        community=community
    ).exists()

    if not is_member:
        return redirect(
            "community_detail",
            slug=slug
        )

    if request.method == "POST":

        form = CommunityMessageForm(request.POST)

        if form.is_valid():

            message = form.save(commit=False)

            message.community = community

            message.sender = request.user

            message.save()

            return redirect(
                "community_chat",
                slug=slug
            )

    else:

        form = CommunityMessageForm()

    messages = CommunityMessage.objects.filter(
        community=community
    )

    return render(
        request,
        "community/community_chat.html",
        {
            "community": community,
            "messages": messages,
            "form": form,
        },
    )

@login_required
def community_feed(request, slug):

    community = get_object_or_404(
        Community,
        slug=slug
    )

    is_member = Membership.objects.filter(
        user=request.user,
        community=community
    ).exists()

    if not is_member:
        return redirect(
            "community_detail",
            slug=slug
        )

    community_posts = Post.objects.filter(
        community=community
    ).order_by("created_at")   # <-- Add/change this here

    return render(
        request,
        "community/community_feed.html",
        {
            "community": community,
            "community_posts": community_posts,
        }
    )

