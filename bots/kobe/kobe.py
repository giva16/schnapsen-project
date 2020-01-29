"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""

# Import the API objects
from api import State, util
from api import Deck
import random

class Bot:

	__max_depth = -1
	__randomize = True

	def __init__(self, randomize=True, depth=6):
	
		self.__randomize = randomize
		self.__max_depth = depth

		self.trump_suit_moves = []


	def get_move(self, state):

		moves = state.moves()
		chosen_move = moves[0]

		for move in moves: # Get cards with trump suit
			if move[0] and Deck.get_suit(move[0]) == state.get_trump_suit():
				self.trump_suit_moves.append(move)

		# PHASE 1
		if state.get_phase() == 1:
			move_trump_suit = []
			
			for index, move in enumerate(moves):
				if move[0] is not None and Deck.get_suit(move[0]) == state.get_trump_suit():
					if move[0] % 5 == 0:
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

		# PHASE 2: Use minimax without alphabeta pruning
		else:
			bes_val, best_move = self.value(state)
			return best_move


	def __before_phase_2(self, state, moves, opp_card):
		highest_move = (None, None)
		for move in moves:
			# Play highest card with the same suit as the opponent's card
			if move[0] is not None and opp_card is not None: 
				if Deck.get_suit(move[0]) == Deck.get_suit(opp_card) and opp_card % 5 > move[0] % 5:
					return move

				# Play a trump suited card with the highest rank card to get the lead in phase 2
				elif len(self.trump_suit_moves) > 0:
					return self.__highest_card(self.trump_suit_moves)
				
				# Play highest card
				else:
					return self.__highest_card(moves)

		return chosen_move


	def __lead_before_phase_2(self, state, moves):
		# Play a trump suited card with the highest rank garauntee to get the lead in phase 2
		if len(self.trump_suit_moves) > 0:
			return self.__highest_card(self.trump_suit_moves)
		else:
			return self.__highest_card(moves)


	def __lowest_card(self, moves):
		lowest_move = (0, None) #Ace
		for move in moves:
			if move[0] is not None and lowest_move[0] % 5 < move[0] % 5:
				lowest_move = move
		return lowest_move


	def __highest_card(self, moves):
		highest_move = (4, None) #Jack
		for move in moves:
			if move[0] is not None and (highest_move[0] % 5 > move[0] % 5):
				highest_move = move
		return highest_move


	def value(self, state, depth = 0): # type: (State, int) -> tuple[float, tuple[int, int]]

		# Base case: No more cards need to be search in the heuristic tree 
		# Because game is finished, no more cards left
		if state.finished():
			winner, points = state.winner()
			return (points, None) if winner == 1 else (-points, None)

		# Base case: No more cards need to be searched in our Deck
		# Because best move found
		if depth == self.__max_depth:
			return heuristic(state)

		moves = state.moves()

		if self.__randomize:
			random.shuffle(moves)

		best_value = float('-inf') if maximizing(state) else float('inf')
		best_move = None

		for move in moves:
			next_state = state.next(move)
		
		# IMPLEMENT: Add a recursive function call so that 'value' will contain the
		# minimax value of 'next_state'
		# 
		value, _ = self.value(next_state, depth + 1)

		# MAX's turn to play
		if maximizing(state):
			if value > best_value:
				best_value = value
				best_move = move

		# MIN's turn to play
		# else:
		if value < best_value:
			best_value = value
			best_move = move

		return best_value, best_move


def maximizing(state): # type: (State) -> bool
	return state.whose_turn() == 1


def heuristic(state): # type: (State) -> float
	# return state.get_trump_or_ace(state), None
	return util.get_number_trumps_or_ace(state,Deck) * 2.0 - 1.0, None
