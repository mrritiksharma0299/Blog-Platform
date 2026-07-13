from django import forms
from .models import Community, CommunityMessage


class CommunityForm(forms.ModelForm):

    class Meta:
        model = Community

        fields = [
            "name",
            "description",
            "image",
        ]


class CommunityMessageForm(forms.ModelForm):

    class Meta:
        model = CommunityMessage

        fields = [
            "message",
        ]

        widgets = {
            "message": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Type your message..."
                }
            )
        }