from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    """Stores the data for posts."""
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISH = 'PB', 'Publish'


    #Fields 
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
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

    class Meta:
        """Adding some aditional settings to the model."""
        # Defining the field and order to be presented the data
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
        


    def __str__(self):
        """Return a string represantantion of the Post"""
        return self.title