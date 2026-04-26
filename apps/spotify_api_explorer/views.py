from typing import List

from django.shortcuts import render

from .services import get_songs


def login_view(request):
    return render(request, 'base.html')


def songs_view(request):
    songs: List = get_songs(request)
    return render(request, 'songs.html', {'songs': songs})
