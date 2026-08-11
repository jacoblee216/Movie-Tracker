from django.contrib import admin
from .models import Song, Playlist, AppUser, SpotifyAccount
# Register your models here.
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(AppUser)
admin.site.register(SpotifyAccount)