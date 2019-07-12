"""
This is the code for the UCT (Upper Confidence Bounds for Trees)
algorithm.
"""

from ai.node import Node
import copy
import math
import random
from time import process_time


def get_best_move(cur_state, reward_function):
    """
    With this function, we will try to get the best move.
    """
    return _uct_search(cur_state, reward_function)


def _uct_search(game_state, reward_function):
    """
    We do this in order to get the action that leads to the node child with the best reward (optimal move).
    """        
    root = Node(game_state)
    root.name = "root"

    best_child_of_root = _search_helper(root, reward_function)
    while _child_is_not_most_visited(best_child_of_root, root):
        best_child_of_root = _search_helper(root, reward_function)

    best_move = best_child_of_root.move_that_derived_this_node()
    return best_move


def _search_helper(root, reward_function):
    start_time = process_time()
    while _within_computational_budget(start_time):
        v = _tree_policy(root)
        delta = _default_policy(v.state, reward_function)
        _back_up(v, delta)
    best_child_of_root = _best_child(root)
    return best_child_of_root


def _child_is_not_most_visited(child, root):
    children = root.children
    for c in children:
        if c is not child:
            if c.num_times_visited > child.num_times_visited:
                return True
    return False



def _back_up(v, delta):
    """
    With this function we get, Delta which is the value of the terminal node that we reached through the node V.
    """
    while v is not None:
        v.num_times_visited += 1
        v.total_reward += _delta_function(delta, v)
        v = v.parent


def _best_child(v):
    assert(len(v.children) != 0)
    c =  math.sqrt(2)
    #We use c = sqrt(2), because that it its theorical value for the MCT.

    def valfunc(v_prime, v):
        left = v_prime.total_reward / v_prime.num_times_visited
        right = c * math.sqrt((math.log(v.num_times_visited)) / v_prime.num_times_visited)
        return left + right

    values_and_nodes = [(valfunc(v_prime, v), v_prime) for v_prime in v.children]
    max_tup = max(values_and_nodes, key=lambda tup: tup[0])


    for tup in values_and_nodes:
        if tup == max_tup:
            return tup[1]



def _choose_untried_action_from(available_actions, already_chosen_actions):
    """
    This function helps us to choose an un-tried action, rather than a random or uniform one.
    """
    actions_to_choose_from = [a for a in available_actions if a not in already_chosen_actions]
    return random.choice(actions_to_choose_from)


def _default_policy(game_state, reward_function):
    """
    When ever we can not compute the optimal move, we need a default policy. 
    A random choice to follow.
    """
    while not game_state.game_over():
        action = random.choice(game_state.possible_moves())
        game_state = copy.deepcopy(game_state)
        game_state.take_turn(action)
    return reward_function(game_state)


def _delta_function(delta, v):
    """
    Denotes the component of the reward vector delta associated
    with the current player p at node v.
    """
    return delta


def _expand(v):
    """
    This function helps us expand the MC Tree with all possible actions that we can do.
    """
    available_actions = v.available_actions()
    already_tried = v.already_tried_actions
    action_to_try = _choose_untried_action_from(available_actions, already_tried)
    v_prime = v.derive_child(action_to_try)
    return v_prime


def _tree_policy(v):
    """
    This is a complementary function to the above one.
    Here we check if the node we're in is terminal or not, if not, keep expanding.
    """
    while v.is_non_terminal():
        if v.is_not_fully_expanded():
            return _expand(v)
        else:
            v = _best_child(v)
    return v


def _within_computational_budget(start):
    """
    With this function, we can control the time in which our algorithm convergs.
    The more we add more time to the algorithm, the harder it will be to beat it.
    """
    elapsed_time = process_time() - start
    return elapsed_time < 2



