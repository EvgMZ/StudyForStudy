from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

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
'''CRUD операции
Create 
Model.objects.create()
Read
Models.objects.get(id = N)

Update
object.property = 'new_value'
Delete
object.delete()'''