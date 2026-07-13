from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email"
            }
        )
    )


    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": field.replace("_", " ").title()
                }
            )

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            "profile_image",
            "bio",
            "country",
            "website",
            "github",
            "linkedin",
        ]


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]