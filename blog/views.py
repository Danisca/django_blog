from django.shortcuts import render
from django.http import Http404
from .models import Post


def post_list(request):
    """Retrieves the list of published posts."""

    posts = Post.published.all()
    return render(
        request, 
        'blog/post/list.html',
        {'posts':posts}
    )


def post_detail(request, id):
    """Retrieves the details of a specific Post."""
    try:
        post = Post.published.get(id= id)
    except Post.DoesNotExist:
        raise Http404('No post found.')
    
    return render(
        request,
        'blog/post/detail.html',
        {'post':post}
    )
