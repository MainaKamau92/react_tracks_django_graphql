from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class Track(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

class Likes(models.Model):
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    track = models.ForeignKey('musics.Track', related_name='likes', on_delete=models.CASCADE)