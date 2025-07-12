from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    """Create the form to share posts via email."""
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        widget= forms.Textarea
    )


class CommentForm(forms.ModelForm):
    """Create the html form for Comment model."""
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        