from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        # exclude = ('post', 'author', 'crated_at', 'updated_at')