from django.shortcuts import render

from gameplay.models import Game


def home(request):
    """
    Player home view function
    :param request: request context
    :return: render player home page
    """
    my_games = Game.objects.games_for_user(request.user)
    active_games = my_games.active()

    return render(request, 'player/home.html', {
        'games': active_games
    })
