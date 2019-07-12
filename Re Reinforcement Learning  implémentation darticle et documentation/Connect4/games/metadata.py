class MetaData:
    """
    The meta data required for the game.
    """
    
    def __init__(self):
        self.player_symbol = None
        self.player_goes_first = False
        self.ai_symbol = None

    def get_next_request_str(self):
        if not self.player_symbol:
            self._request = "self.player_symbol"
            return "Choose your symbol ( x or o ) :"



    def needs_more_metadata(self):
        if not self.player_symbol:
            return True
        elif self.player_goes_first is None:
            return True
        else:
            return False

    def set_next_metadata(self, d):
        """
        This requires that d is clean already.
        """
        if self._request == "self.player_symbol":
            self.player_symbol = d
            if d == 'x':
                self.ai_symbol = 'o'
            else:
                self.ai_symbol = 'x'
        elif self._request == "self.player_goes_first":
            self.player_goes_first = True if d == 'y' else False


    def valid(self, d):
        """
        Checks if d is valid, given the last item to be requested.
        """
        if self._request == "self.player_symbol":
            return d == "x" or d == "o" or d == "X" or d == "O"
        elif self._request == "self.player_goes_first":
            return d == "y" or d == "Y" or d == "n" or d == "N"

