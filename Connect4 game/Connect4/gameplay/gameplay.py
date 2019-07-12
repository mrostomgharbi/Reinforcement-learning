ai_module = None
game_module = None


def start_game():
    """
    This is the main entry to the game. 
    We will need here both the game module and the ai module in order to run everything together.
    """
    global ai_module
    global game_module

    print("\nThis game is developped to show how the MCTs work with games.\n")
    print("------------------------------------------")
    print("This application is developped by : \n")
    print("\t BEJAOUI Ahmed")
    print("\t GHARBI Mohamed Rostom")
    print("\t MEJRI Aymen \n")
    print("------------------------------------------")

    print(game_module.welcome_string())

    while game_module.needs_more_metadata():
        d = _get_next_metadata()
        while game_module.metadata_not_valid(d):
            d = _get_next_metadata()
        game_module.set_next_metadata(d)

    game_module.initialize(ai_module)

    while not game_module.game_over():
        state_to_display = game_module.get_formatted_display()
        print(state_to_display)
        if game_module.players_turn():
            _do_players_turn()
        else:
            game_module.take_ai_turn()

    ending_state = game_module.get_formatted_display()
    print(ending_state)

    ending_message = game_module.get_ending_msg()
    print(ending_message)


def _do_players_turn():
    while game_module.needs_more_player_input():
        info = _get_next_input()
        invalid_move, err_msg = game_module.info_not_valid(info)
        while invalid_move:
            print(err_msg)
            info = _get_next_input()
            invalid_move, err_msg = game_module.info_not_valid(info)
        game_module.set_next_input(info)
    game_module.take_player_turn()

def _get_next_metadata():
    request_str = game_module.get_next_metadata_request_str()
    d = input(request_str)
    return d

def _get_next_input():
    input_request_str = game_module.get_input_request_str()
    info = input(input_request_str)
    return info




