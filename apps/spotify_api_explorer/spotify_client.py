from typing import Optional

import requests
from allauth.socialaccount.models import SocialToken


def get_top_tracks(token: Optional[SocialToken], time_range: str = 'medium_term', limit: int = 50):
    if token:
        headers = {'Authorization': f'Bearer {token.token}'}
        params = {'time_range': time_range, 'limit': limit}
        response = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers, params=params)
        return response.json()
    return None
