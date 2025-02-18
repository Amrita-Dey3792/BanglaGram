from django import forms
from Posts.models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author', 'view_count', 'liked_users')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)




