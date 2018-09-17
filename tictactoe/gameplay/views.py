from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic.list import ListView

from .models import Game
from .forms import MoveForm


@login_required
def game_detail(request, id):
    """
    Game details view function
    :param request: request context
    :return: game details view
    """
    game = get_object_or_404(Game, pk=id)
    context = { 'game': game}

    if game.is_user_move(request.user):
        context['form'] = MoveForm()

    return render(request, 'gameplay/game_detail.html', context)


@login_required
def make_move(request, id):
    """
    Make move view function
    :param request: request context
    :param id: id of game
    :return: game details view with latest move made
    """
    game = get_object_or_404(Game, pk=id)

    if not game.is_user_move(request.user):
        raise PermissionDenied

    move = game.new_move()
    form = MoveForm(instance=move, data=request.POST)

    if form.is_valid():
        move.save()
        return redirect('gameplay_detail', id)
    else:
        return render(request, 'gameplay/game_detail.html', {
            'game': game,
            'form': form
        })


class AllGamesList(ListView):
    """
    List all games view class
    """
    model = Game
