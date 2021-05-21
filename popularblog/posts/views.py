from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import PostForm
from .models import Group, Post


def index(request):
    latest = Post.objects.order_by('-pub_date')[:10]
    return render(
        request,
        'index.html',
        {'posts' : latest}
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