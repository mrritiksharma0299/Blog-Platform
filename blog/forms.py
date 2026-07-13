from django import forms
from .models import Post, CATEGORY_CHOICES, Comment
from community.models import Community


class PostForm(forms.ModelForm):

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES
    )

    other_category = forms.CharField(
        required=False
    )

    visibility = forms.ChoiceField(
        choices=Post.VISIBILITY_CHOICES
    )

    community = forms.ModelChoiceField(
        queryset=Community.objects.all(),
        required=False,
        empty_label="Select Community"
    )

    class Meta:
        model = Post

        fields = [
            "title",
            "country",
            "category",
            "other_category",
            "visibility",
            "community",
            "featured_image",
            "content",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        category = cleaned_data.get("category")
        other = cleaned_data.get("other_category")

        if category == "Other":
            if not other:
                self.add_error(
                    "other_category",
                    "Please enter a category."
                )

        visibility = cleaned_data.get("visibility")
        community = cleaned_data.get("community")

        if visibility == "community" and not community:
            self.add_error(
                "community",
                "Please choose a community."
            )

        return cleaned_data


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment

        fields = ["text"]

        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write a comment..."
                }
            )
        }

        labels = {
            "text": ""
        }