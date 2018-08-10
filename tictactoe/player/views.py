from django.shortcuts import render

from gameplay.models import Game


def home(request):
    return render(request, 'player/home.html', {
        'number_of_games': Game.objects.count()
    })
