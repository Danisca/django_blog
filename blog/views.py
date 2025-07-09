from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post
from .forms import EmailPostForm


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

#Class-based views
class PostListView(ListView):
    """Class-based List-view of posts."""
    queryset = Post.published.all()
    paginate_by = 3
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    """Allows post sharing via email."""
    post = get_object_or_404(
        Post,
        id=post_id,
        status= Post.Status.PUBLISHED
    )
    sent = False

    if request.method == 'POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data #parameters validated
            name = cleaned_data['name']
            email = cleaned_data['email']
            comments = cleaned_data['comments']
            recipients = [cleaned_data['to']]# this field must be a tuple or a list

            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (f"{name} {email} "
                       f"recomends you read, {post.title}")
            message = (f"Read {post.title} at {post_url}\n\n"
                f"{name}'s comments: {comments}")
            
            send_mail(subject, message,from_email=None,recipient_list=recipients)
            sent = True
    else:
        form = EmailPostForm()

    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form':form,
            'sent':sent
        }
    )