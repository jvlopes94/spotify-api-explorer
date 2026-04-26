from allauth.socialaccount.models import SocialToken

from .spotify_client import get_top_tracks


def get_songs(request):
    token = SocialToken.objects.filter(
        account__user=request.user,
        account__provider='spotify'
    ).first()
    data = get_top_tracks(token=token, time_range='medium_term', limit=50)
    songs = data.get('items', []) if data else []
    return songs
