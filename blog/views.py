from django.shortcuts import render, get_object_or_404
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
    post = get_object_or_404(
        Post,
        id= id,
        status= Post.Status.PUBLISH
    )
    
    return render(
        request,
        'blog/post/detail.html',
        {'post':post}
    )
