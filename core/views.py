from django.shortcuts import render


def about_view(request):
    return render(request, "footer/about.html")


def contact_view(request):
    return render(request, "footer/contact.html")


def help_center_view(request):
    return render(request, "footer/help_center.html")


def privacy_policy_view(request):
    return render(request, "footer/privacy_policy.html")


def terms_of_service_view(request):
    return render(request, "footer/terms_of_service.html")