from django.db import models

from user.models import CustomUser


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.ManyToManyField(
        CustomUser, related_name="liked_posts", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
