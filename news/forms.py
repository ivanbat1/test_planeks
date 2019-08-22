import datetime

from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Post, Comment
from user.models import AppUser


class CreatePostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    date_create = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'],
                                      widget=forms.DateTimeInput(
                                          attrs={
                                              'type': 'datetime-local',
                                              'class': 'input-date form-control'},
                                          format='%Y-%m-%dT%H:%M'))

    class Meta:
        model = Post
        fields = ('title', 'content', 'url', 'date_create')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', 'parent')
