from .models import AppUser, SpotifyAccount
import requests
from django.conf import settings
from datetime import datetime, timezone, timedelta


def exchange_code_for_tokens(callback_code, user):
    response = requests.post(
    "https://accounts.spotify.com/api/token",   # URL — this is Spotify's fixed endpoint for token exchange
    data={                                        # the BODY of the request — form fields Spotify expects
        "grant_type": "authorization_code",
        "code": callback_code,
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "client_secret": settings.SPOTIFY_CLIENT_SECRET,
    },
)
    if response.status_code != 200:
        print(response.text)
    else:
        token_data = response.json()
        
        SpotifyAccount.objects.update_or_create(
            user=user,
            access_token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
            token_expires_at=timezone.now() + timedelta(seconds=token_data["expires_in"]),
            spotify_id = token_data["spotify_id"],
            spotify_name = token_data["display_name"]
        )