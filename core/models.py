from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length = 25)
    genres = models.JSONField(default=list)


class AppUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password_hash=models.CharField(max_length=255)
    date_joined=models.DateTimeField(auto_now_add=True)
    movie_list = models.ManyToManyField(Movie, related_name="liked_by", blank=True)

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)
    

