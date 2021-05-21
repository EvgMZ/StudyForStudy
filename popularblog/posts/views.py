from typing_extensions import Required
from django.contrib.auth import load_backend, login
from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.decorators.cache import cache_page
from .forms import PostForm, CommentForm
from .models import Group, Post, Follow
from django.contrib.auth.models import User
from django.core.paginator import Paginator
@cache_page(20, key_prefix='index_page')
def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page' : page, 'paginator' : paginator}
    )
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.grposts.all()
    return render(
        request,
        'group.html',
        {'group':group, 'posts':posts}
    )

class NewPost(CreateView):
    form_class = PostForm
    success_url = reverse_lazy('new')
    template_name = 'new.html'

@login_required()
def new_post(request):
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'new.html', {'form':form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('index')


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post = author.author_posts.all()
    paginator = Paginator(post, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    following = False
    if request.user.is_authenticated:
        if Follow.objects.filter(
            user=User.objects.get(
                username=request.user
                ),
                author=User.objects(
                    username=username
                )
                ).exists():
            following = True
    return render(
        request,'profile.html',
    {
        'author' : author,
        'paginator' : paginator,
        'following' : following,
        'post' : post,
        'page' : page
    }
    )

def post_view(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    auhtor = post.author
    form = CommentForm()
    comments = post.comment.all()

@login_required
def post_edit(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id = post_id, author__username = username)
    if request.user != profile:
        return redirect ('post', username=username, post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
        )
    if form.is_valid():
        form.save()
        return redirect('post', username=request.user.username,
        post_id=post_id)
    return render (request,'post_new.html',{'form' : form, 'post':post})

@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, auhtor__username=username, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect('post', username=username, post_id=post_id)

@login_required
def follow_index(request):
    post = Post.objects.filter(author__followin__user=request.user)
    paginator = Paginator(post, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'follow.html',
        {'post' : post,
        'page' : page,
        'paginator' : paginator
        }
    )