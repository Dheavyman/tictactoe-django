from django.shortcuts import render, redirect


def welcome(request):
    """
    Tictactoe home view function
    :param request: request context
    :return: render welcome page
    """
    if request.user.is_authenticated:
        return redirect('player_home')
    else:
        return render(request, 'tictactoe/welcome.html')
