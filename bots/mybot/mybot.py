"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""

# Import the API objects
from api import State
from api import Deck
import random


class Bot:

    def __init__(self):
        pass

    def get_move(self, state):
        # type: (State) -> tuple[int, int]
        """
        Function that gets called every turn. This is where to implement the strategies.
        Be sure to make a legal move. Illegal moves, like giving an index of a card you
        don't own or proposing an illegal mariage, will lose you the game.
       	TODO: add some more explanation
        :param State state: An object representing the gamestate. This includes a link to
            the states of all the cards, the trick and the points.
        :return: A tuple of integers or a tuple of an integer and None,
            indicating a move; the first indicates the card played in the trick, the second a
            potential spouse.
        """

        # All legal moves
        moves = state.moves()
        chosen_move = moves[0]

        move_trump_suit = []

        for index, move in enumerate(moves):
            if move[0] is not None and Deck.get_suit(move[0]) == state.get_trump_suit():
                move_trump_suit.append(move)

        if len(move_trump_suit) > 0 :
            chosen_move = move_trump_suit[0]
            return chosen_move

        if state.get_opponents_played_card() is not None :

            move_same_suit = []
            move_lowest = []

            for index, move in enumerate(moves):

                if Deck.get_suit(move[0]) == Deck.get_suit(state.get_opponents_played_card()):
                    if move[0] is not None and move[0] % 5 < state.get_opponents_played_card() % 5 :
                        move_same_suit.append(move)

                elif move[0] is not None and move[0] % 5 > chosen_move[0] % 5:
                    move_lowest.append(move)

            if len(move_same_suit) > 0 :
                chosen_move = move_same_suit[0]
                return chosen_move

            elif len(move_lowest) > 0 :
                chosen_move = move_lowest[0]
                return chosen_move

        for index, move in enumerate(moves):
            if move[0] is not None and move[0] % 5 <= chosen_move[0] % 5:
                chosen_move = move

        # Return a random choice
        return chosen_move


