from datetime import datetime
from ckeditor.fields import RichTextField
from django.db import models

# Create your models here.
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Post(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)
    author = models.ForeignKey('user.AppUser', on_delete=models.CASCADE, related_name='author')
    content = RichTextField()
    date_create = models.DateTimeField(null=True, blank=True, editable=True)
    url = models.URLField(max_length=250, blank=True, null=True)
    subscribe = models.ManyToManyField('user.AppUser', related_name='users_subscribe')

    def get_absolute_url(self):
        return reverse('home')

    def __str__(self):
        return '{}'.format(self.title)

    def as_json(self):
        context = {}
        for key, value in self.__dict__.items():
            if key != "_state":
                context[key] = value
        return context


class Comment(MPTTModel):
    posting = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey('user.AppUser', on_delete=models.CASCADE)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE, db_index=True)
    comment = models.CharField(max_length=256, blank=True, null=True)

    def as_json(self):
        context = {}
        for key, value in self.__dict__.items():
            if key != "_state":
                context[key] = value
        return context
