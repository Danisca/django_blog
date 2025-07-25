from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.db.models import Count
from taggit.models import Tag
from .models import Post
from .forms import EmailPostForm, CommentForm


def post_list(request, tag_slug=None):
    """Retrieves the list of published posts."""

    posts_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(
            Tag,
            slug= tag_slug
        )
        posts_list = posts_list.filter(tags__in = [tag])
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
        {
            'posts':posts,
            'tag':tag
         }
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
    #getting all comments with active = true
    comments = post.comments.filter(active=True)
    #form for users to comment
    form = CommentForm()
    
    #retrieving posts related by tags

    post_tags_ids = post.tags.values_list('id', flat=True)# getting all the ids of each tag associated to the post
    similar_posts = Post.objects.filter(
        tags__in = post_tags_ids
    ).exclude(id=post.id) # get all the posts that have the same tags of the current post

    similar_posts = similar_posts.annotate(
        same_tags = Count('tags')
    ).order_by('-same_tags','-publish')[:4]

    return render(
        request,
        'blog/post/detail.html',
        {
            'post':post,
            'comments':comments,
            'form':form,
            'similar_posts': similar_posts
         }
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


@require_POST #This decorator forces the view to use only POST method
def post_comment(request, post_id):
    """Add a new comment to a specific post."""
    post = get_object_or_404(
        Post,
        id=post_id,
        status= Post.Status.PUBLISHED
    )
    comment = None
    # a comment was posted
    form = CommentForm(data= request.POST)
    if form.is_valid():
        comment = form.save(commit=False) # create an instance of the Model without saving it
        comment.post = post #assign the post to the comment
        comment.save() # save the comment to the database
    
    return render(
        request,
        'blog/post/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment
        }
    )
