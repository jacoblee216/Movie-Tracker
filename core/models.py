from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length = 25)
    genres = models.JSONField(default=list)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    movie_list = models.ManyToManyField(Movie, related_name="liked_by", blank=True)
