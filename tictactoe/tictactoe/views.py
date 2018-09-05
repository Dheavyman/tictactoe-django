from django.shortcuts import render


def welcome(request):
    """
    Tictactoe home view function
    :param request: request context
    :return: render welcome page
    """
    return render(request, 'tictactoe/welcome.html')
