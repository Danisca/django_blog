from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    """Retrieves the list of published posts."""

    posts_list = Post.published.all()
    paginator = Paginator(posts_list,3)# pagination with 3 post per page
    page_number = request.GET.get('page', 1)
    
    try:
       
        posts = paginator.page(page_number)

    except EmptyPage:
        #if the number is out of range show the las page
        # paginator.num_pages = last page
        posts = paginator.page(paginator.num_pages)
    
    # in the case page parameter is not an integer example  example.com/?page=asdf
    except PageNotAnInteger:
        posts = paginator.page(1)


    return render(
        request, 
        'blog/post/list.html',
        {'posts':posts}
    )


def post_detail(request, year, month, day, post):
    """Retrieves the details of a specific Post."""
    post = get_object_or_404(
        Post,
        status= Post.Status.PUBLISHED,
        slug= post,
        publish__year = year,
        publish__month= month,
        publish__day = day
        
    )
    
    return render(
        request,
        'blog/post/detail.html',
        {'post':post}
    )
