from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    """A article the user is writing about"""
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateField(auto_now_add=True)
    last_date = models.DateField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of model."""
        return self.subject


class Comment(models.Model):
    """Something specific comment about a article."""
    content = models.TextField()
    create_date = models.DateField(auto_now_add=True)
    last_date = models.DateField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of model."""
        return self.content
