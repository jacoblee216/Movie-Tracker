from .models import AppUser, SpotifyAccount
import requests
from django.conf import settings
from datetime import timedelta
from django.utils import timezone


def exchange_code_for_tokens(callback_code, user): # need to write another request for display_name and spotify_id
    response = requests.post(
    "https://accounts.spotify.com/api/token",   # URL — this is Spotify's fixed endpoint for token exchange
    data={                                        # the BODY of the request — form fields Spotify expects
        "grant_type": "authorization_code",
        "code": callback_code,
        "redirect_uri": settings.REDIRECT_URI,
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
    },
)

    if response.status_code != 200:
        print("General response failed")
        print(response.text)
        return False
    else:
        token_data = response.json()

        user_response = requests.get( 
        "https://api.spotify.com/v1/me",
        headers={"Authorization": f"Bearer {token_data['access_token']}"},
    )
        if user_response.status_code != 200:
            print("User response failed")
            print(user_response.text)
            return False
        
        user_data = user_response.json()
        spotify_account, created = SpotifyAccount.objects.update_or_create(
            user=user,  # lookup field — find the existing row for this user (or create one)
            defaults={   # fields to set/update on that row
                "access_token": token_data["access_token"],
                "refresh_token": token_data["refresh_token"],
                "token_expires_at": timezone.now() + timedelta(seconds=token_data["expires_in"]),
                "spotify_id": user_data["id"],
                "spotify_name": user_data.get("display_name", ""),
                "country": user_data.get("country",""),
                "profile_image_url": user_data["images"][0]["url"] if user_data.get("images") else "",

            },
        )
        print(f"profile_image_url = '{spotify_account.profile_image_url}'")
        return True