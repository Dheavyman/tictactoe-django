from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import  MinValueValidator, MaxValueValidator

GAME_STATUS_CHOICES = (
    ('F', 'First Player To Move'),
    ('S', 'Second Player To Move'),
    ('W', 'First Player Wins'),
    ('L', 'Second Player Wins'),
    ('D', 'Draw')
)

BOARD_SIZE = 3


class GameQuerySet(models.QuerySet):
    """
    Game custom query set
    """
    def games_for_user(self, user):
        return self.filter(
            Q(first_player=user) | Q(second_player=user)
        )

    def active(self):
        return self.filter(
            Q(status='F') | Q(status='S')
        )


class Game(models.Model):
    """
    Game model
    """
    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, default='F',
                              choices=GAME_STATUS_CHOICES)

    first_player = models.ForeignKey(User, related_name='games_first_player',
                                     on_delete=models.CASCADE)
    second_player = models.ForeignKey(User, related_name='games_second_player',
                                      on_delete=models.CASCADE)
    objects = GameQuerySet.as_manager()

    def get_absolute_url(self):
        """
        Get the url of a game model instance
        :return: game model instance url
        """
        return reverse('gameplay_detail', args=[self.id])

    def board(self):
        """
        Shows a 2-dimensional list of move objects with the state of a square
        at position [y][x].
        :return: board structure
        """
        board = [[None for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        for move in self.move_set.all():
            board[move.y][move.x] = move

        return board

    def is_user_move(self, user):
        """
        Check if it's users turn to make a move
        :return: True or False
        """
        return (user == self.first_player and self.status == 'F') or\
               (user == self.second_player and self.status == 'S')

    def new_move(self):
        """
        New player move
        :return: move object with player, game and count preset
        """
        if self.status not in 'FS':
            raise ValueError('Cannot make move on finished game.')

        return Move(game=self, by_first_player=self.status == 'F')

    def update_after_move(self, move):
        """
        Update the status of game after player move
        :param move: last move made by player
        :return: None
        """
        self.status = self._get_game_status_after_move(move)

    def _get_game_status_after_move(self, move):
        """
        Get the status of game after player move
        :param move: last move made by player
        :return: new game status after a move
        """
        x = move.x
        y = move.y
        board = self.board()

        if (board[y][0] == board[y][1] == board[y][2]) or\
            (board[0][x] == board[1][x] == board[2][x]) or\
            (board[0][0] == board[1][1] == board[2][2] and
             board[0][0] is not None) or\
            (board[0][2] == board[1][1] == board[2][0] and
             board[0][2] is not None):
                return 'W' if move.by_first_player else 'L'
        if self.move_set.count() >= BOARD_SIZE * 2:
            return 'D'
        return 'S' if self.status == 'F' else 'F'

    def __str__(self):
        return f'{self.first_player} vs {self.second_player}'


class Move(models.Model):
    """
    Move model
    """
    x = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(BOARD_SIZE - 1)]
    )
    y = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(BOARD_SIZE - 1)]
    )
    comment = models.CharField(max_length=300, blank=True)
    by_first_player = models.BooleanField(editable=False)

    game = models.ForeignKey(Game, on_delete=models.CASCADE, editable=False)

    def __eq__(self, other):
        if other is None:
            return False

        return other.by_first_player == self.by_first_player

    def save(self, *args, **kwargs):
        super(Move, self).save(*args, **kwargs)
        self.game.update_after_move(self)
        self.game.save()
