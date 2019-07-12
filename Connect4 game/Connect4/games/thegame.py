from games.metadata import MetaData
from games.gamestate import GameState
import os

# Global variables
_metadata = MetaData()
_gamestate = None

def game_over():
    """
    Returns True if the game is over, False if it is not the case.
    """
    return _gamestate.game_over()


def get_ending_msg():
    """
    Returns the ending message (such as who won).
    """
    winner = _gamestate.get_winner()
    if winner == ' ':
        s = "IT'S A DRAW" + os.linesep
    else:
        s = '\n---------------------------------------------\n\n'
        s += winner + " have 4 in a row. \n" 
        s += winner + ' wins this game !' + os.linesep
    s += "\nClick on the UP arrow button then press ENTER for another game.\n"
    return s


def get_formatted_display():
    """
    This function returns the state of the game as a string which will be printed
    on the console for the user.
    """
    return _gamestate.get_formatted_display()


def get_input_request_str():
    """
    This function returns a string that the UI should print in order to request
    the next player turn information.
    """
    return _gamestate.get_next_input_request_str()


def get_next_metadata_request_str():
    """
    This function returns a string that the UI should print in order to request
    the next metadata variable that the game requires.
    """
    global _metadata
    return _metadata.get_next_request_str()


def info_not_valid(info):
    """
    This function returns True if the given info is NOT valid for the game state's
    current request for player info.
    """
    valid, err_msg = _gamestate.info_valid(info)
    return (not valid, err_msg)


def initialize(ai_module):
    global _gamestate
    _gamestate = GameState(_metadata, ai_module)


def metadata_not_valid(d):
    """
    This function eturns True if the data item is NOT valid.
    """
    return not _metadata.valid(d)


def needs_more_metadata():
    """
    This function returns whether or not the game logic requires any more meta data.
    """
    return _metadata.needs_more_metadata()


def needs_more_player_input():
    """
    This function returns whether or not the game logic requires any more player input
    to execute the players turn.
    """
    return _gamestate.needs_more_player_input()


def players_turn():
    """
    This function returns True if it is the player's turn, Flase if its not.
    """
    return _gamestate.players_turn


def set_next_input(info):
    """
    Next item in the game state.
    """
    _gamestate.set_next_input(info)


def set_next_metadata(d):
    """
    Next item to d in the game's meta data.
    """
    _metadata.set_next_metadata(d)


def take_ai_turn():
    """
    This function modifies the game state in order that the computer take his turn.
    """
    _gamestate.take_ai_turn()


def take_player_turn():
    """
    This function modifies the game state in order that the player take his turn.
    """
    _gamestate.take_player_turn()


def welcome_string():
    """
    First string to be displayed after game opening.
    """
    return "Let the game begins ! \n \nGood luck !\n"









