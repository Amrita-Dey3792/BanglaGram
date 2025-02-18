from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
import os
from django.db.models.signals import post_delete
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile, File


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='Posts/post_images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    view_count = models.PositiveBigIntegerField(default=0)
    liked_users = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
    
@receiver(post_delete, sender=Post)
def delete_post_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Add Comment")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    

    









        
