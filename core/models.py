from django.db import models
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.
class Song(models.Model):
    name = models.CharField(max_length = 25)
    genres = models.JSONField(default=list)

class AppUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password_hash=models.CharField(max_length=255)
    date_joined=models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

class Playlist(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="playlists")
    name = models.CharField(max_length = 25)
    songs = models.ManyToManyField(Song, related_name="playlists")

class SpotifyAccount(models.Model):
    user = models.OneToOneField(
        AppUser,
        on_delete = models.CASCADE,
        related_name="spotify_account",
    )
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_expires_at = models.DateTimeField()

    follower_count = models.PositiveIntegerField(default=0)
    profile_image_url = models.URLField(blank=True)
    spotify_id = models.CharField(max_length=255,unique=True)
    spotify_name = models.CharField(max_length=25)
    

    connected_at = models.DateTimeField(auto_now_add=True)
    last_refreshed_at = models.DateTimeField(auto_now_add=True)
