from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from gameplay.models import Game
from .models import Invitation
from .forms import InvitationForm


@login_required
def home(request):
    """
    Player home view
    :param request: request context
    :return: render player home page
    """
    my_games = Game.objects.games_for_user(request.user)
    active_games = my_games.active()
    finished_games = my_games.difference(active_games)
    invitations = request.user.invitations_received.all()

    return render(request, 'player/home.html', {
        'active_games': active_games,
        'finished_games': finished_games,
        'invitations': invitations
    })

@login_required
def new_invitation(request):
    """
    Send invitation view
    :param request: request context
    :return: render player invitation form
    """
    if request.method == 'POST':
        invitation = Invitation(from_user=request.user)
        form = InvitationForm(instance=invitation, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_home')
    else:
        form = InvitationForm()

    return render(request, 'player/new_invitation_form.html', { 'form': form })

@login_required
def accept_invitation(request, id):
    """
    Accept invitation view
    :param request: request context
    :param id: id of invitation to accept
    :return: render accept invitation
    """
    invitation = get_object_or_404(Invitation, pk=id)
    if not request.user == invitation.to_user:
        raise PermissionDenied
    if request.method == 'POST':
        if 'accept' in request.POST:
            game = Game.objects.create(
                first_player=invitation.to_user,
                second_player=invitation.from_user
            )
        invitation.delete()
        return redirect(game)
    else:
        return render(request, 'player/accept_invitation_form.html', {
            'invitation': invitation
        })


class SignUpView(CreateView):
    """
    Signup a player view class
    """
    form_class = UserCreationForm
    template_name = 'player/signup_form.html'
    success_url = reverse_lazy('player_home')
