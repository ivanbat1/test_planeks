import datetime

import pytz
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, DetailView
from .forms import CreatePostForm, CommentForm
from .models import Post, Comment
from user.models import AppUser


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'news/home.html'
    login_url = '/user/login/'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(date_create__lte=datetime.datetime.now(pytz.utc).date())
        if self.request.user.is_anonymous:
            context['user'] = 'None'
        else:
            context['user'] = self.request.user
        return context

    def post(self, *args, **kwargs):
        post_subscriber = Post.objects.get(id=self.request.POST.get('pk')).subscribe
        if self.request.user in post_subscriber.all():
            post_subscriber.remove(self.request.user)
            return JsonResponse({'message': 'remove'})
        else:
            post_subscriber.add(self.request.user)
            return JsonResponse({'message': 'add'})


class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = CreatePostForm
    model = Post
    template_name = 'news/create_post.html'
    login_url = '/user/login/'

    def dispatch(self, *args, **kwargs):
        return super(CreatePostView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreatePostView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        form = CreatePostForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = AppUser.objects.get(id=self.request.user.id)
            form.save()
            return JsonResponse({"url": reverse('home')})
        else:
            return JsonResponse({"message": form.errors})


class DetailPost(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news/detail_post.html'
    login_url = '/user/login/'

    def get_context_data(self, **kwargs):
        context = super(DetailPost, self).get_context_data(**kwargs)
        context['posts'] = self.object
        context['comments'] = Comment.objects.filter(posting_id=self.object.id)
        context['form'] = CommentForm()
        return context

    def post(self, request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.posting = Post.objects.get(id=pk)
            comment.author = request.user
            if request.POST.get('parent'):
                comment.parent = Comment.objects.get(id=request.POST.get('parent'))
            form.save()
            return JsonResponse({'url': reverse('detail-post', kwargs={'pk': pk})})
        else:
            return JsonResponse({'message': form.errors})
