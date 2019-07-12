import copy
import os

class Node:
    """
    With this class, we will define different game states as nodes.
    """
    def __init__(self, state):
        self.name = None
        self.state = state
        self.parent = None
        self.children = []
        self.total_reward = 0
        self.num_times_visited = 0
        self.already_tried_actions = []

    def __str__(self):
        s = "Node: "
        for key, val in self.__dict__.items():
            s += os.linesep + "    " + key + ": " + str(val)
        return s

    def available_actions(self):
        """
        This function helps us to get the possible moves given a Node.
        """
        return self.state.possible_moves()

    def derive_child(self, action):
        """
        This function helps us to get a new Node from a current Node given the action we made.
        """
        child_state = copy.deepcopy(self.state)
        child_state.take_turn(action)
        child_node = Node(child_state)
        child_node.parent = self
        child_node.name = self.name + "_" + str(child_node.move_that_derived_this_node())
        self.children.append(child_node)
        self.already_tried_actions.append(action)
        return child_node

    def move_that_derived_this_node(self):
        """
        With this function, we are able to get the action from a Node in the MCT.
        This is an important function since this gives us the optimal play.
        """
        return self.state._move_that_derived_this_state

    def is_non_terminal(self):
        """
        This function returns True, if the node we are in is not terminal.
        A terminal node means that its a node where the game is over.
        """
        return not self.state.game_over()

    def is_not_fully_expanded(self):
        """
        Returns True unless all possible children have been added to this
        Node's childrens.
        """
        return len(self.available_actions()) != len(self.children)







