import copy
from games.board import Board
import os

class GameState:
    """
    This class is developed to hold the intermediate data of the Game.
    """
    def __init__(self, metadata, ai):
        self._metadata = metadata
        self._ai = ai
        self._board = Board()
        self.players_turn = self._metadata.player_goes_first
        self._incoming_move = None
        self._move_that_derived_this_state = None
        self.winner = None

    def __str__(self):
        s = "State: "
        for key, val in self.__dict__.items():
            s += os.linesep + "    " + key + ": " + str(val)
        return s

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k == "_ai":
                setattr(result, k, v)
            else:
                setattr(result, k, copy.deepcopy(v, memo))
        return result

    def current_player_symbol(self):
        """
        This function is developped to get the current player's symbol
        """
        if self.players_turn:
            return self._metadata.players_symbol
        else:
            return self._metadata.ai_symbol

    def game_over(self):
        """
        Output of this function is boolean.
        It returns True if the game is over, False if it is not.
        """
        there_is_a_winner, winner = self._board.four_in_a_row()
        self.winner = winner
        if len(self.possible_moves()) == 0:
            there_is_a_winner = True
            self.winner = ' '
        return there_is_a_winner

    def get_formatted_display(self):
        """
        This function return the current state of the game after that the moves are done,
        and so the player can see it.
        """
        return str(self._board)

    def get_next_input_request_str(self):
        """
        Requests the column number from the player.
        """
        return "Type column number : "

    def get_winner(self):
        """
        Returns the winner of the game or None if there is a draw.
        """
        return self.winner

    def info_valid(self, info):
        """
        This function returns True if the players mouvement is valid.
        Otherwise it displays a message.
        """
        try:
            item = int(info)
            if not self._board.valid_move(item):
                return False, "Please enter a valid column between 0 and 6 "\
                        "that isn't full."
            else:
                return True, ""
        except ValueError:
            return False, "Please enter a valid column between 0 and 6."

    def needs_more_player_input(self):
        """
        Returns True if the GameState object does not have enough
        player input to decide an action for the player.
        """
        return self._incoming_move is None

    def possible_moves(self):
        """
        This function returns a set of all possible legal actions.
        """
        return [move for move in self._action_set() if self._board.valid_move(move)]

    def set_next_input(self, info):
        """
        This function puts into action the players move request only and only if its valid.
        """
        assert(self.info_valid(info))
        self._incoming_move = int(info)

    def take_ai_turn(self):
        """
        Now, it's time for the computer to play.
        """
        move = self._ai.get_best_move(self, _evaluation_function)
        self._board.place(move, self._metadata.ai_symbol)
        self._move_that_derived_this_state = move
        print('--------------------------------------------------------')
        print('\n')
        print('\n')
        print('\nThe robot played its mark in column number : ', move)
        self._incoming_move = None
        self.players_turn = True

    def take_turn(self, move):
        """
        This function can be used to take a turn when the caller does
        not know whose turn it is or does not want to worry about it.
        """
        if self.players_turn:
            self._board.place(move, self._metadata.player_symbol)
            self.players_turn = False
        else:
            self._board.place(move, self._metadata.ai_symbol)
            self.players_turn = True
        self._move_that_derived_this_state = move
        self._incoming_move = None

    def take_player_turn(self):
        """
        Takes the player's turn.
        """
        move = self._incoming_move
        self._board.place(move, self._metadata.player_symbol)
        self._move_that_derived_this_state = move
        self._incoming_move = None
        self.players_turn = False

    def _action_set(self):
        """
        This function generates all possible 6 actions that the computer can play.
        It does not care wether the action is valid or not.
        """
        for c in range(7):
            yield c


def _evaluation_function(state):
    """
    This is the reward function.
    If we ever make the last reward on this function lower, it will be harder to beat the computer.
    """
    reward = 0
    if state._metadata.ai_symbol == 'x' and state.winner == 'x':
        reward = 1.0
    elif state._metadata.ai_symbol == 'o' and state.winner == 'o':
        reward = 1.0
    elif state._metadata.ai_symbol == 'x' and state.winner == 'o':
        reward = 0.0
    elif state._metadata.ai_symbol == 'o' and state.winner == 'x':
        reward = 0.0
    else:
        reward = 0.1

    return reward

