from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


# Create a custom object manager
class PublishedManager(models.Manager):
    """Custom objects manager for published Posts"""
    
    def get_queryset(self):
        return super().get_queryset().filter(status= Post.Status.PUBLISHED)



class Post(models.Model):
    """Stores the data for posts."""
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'


    #Fields 
    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        # Make the slug unique for the publication date.
        unique_for_date='publish'
    )
    #tags field
    tags = TaggableManager()
    #author field
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices= Status,
        default=Status.DRAFT
    )

    #Agregando el custom object manager
    objects = models.Manager()#default manager
    published = PublishedManager()

    class Meta:
        """Adding some aditional settings to the model."""
        # Defining the field and order to be presented the data
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
        

    def get_absolute_url(self):
        """Returning the cannonical url for a specific post."""
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )


    def __str__(self):
        """Return a string represantantion of the Post"""
        return self.title
    

class Comment(models.Model):
    """Defines the structure for comments."""
    
    post = models.ForeignKey(
        Post, 
        on_delete= models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now= True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]


    def __str__(self):
        return f"Comment by {self.name} on {self.created}"