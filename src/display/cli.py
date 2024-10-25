def get_choice(
        options: dict
) -> tuple[str, str] | tuple[int, str]:
    """
    Prompt the user for input and validate it against available options.

     Returns:
        tuple[str, str]: If the user chooses to quit.
        tuple[int, str]: A tuple with the move index and the corresponding move description
                         if a valid move is selected.
    """
    while True:
        user_input = _get_user_input()

        # handle quitting
        if _is_quit(user_input):
            return _handle_quit()

        # handle valid selection
        selection_result = _validate_selection(user_input, options)
        if selection_result:
            return selection_result

        _prompt_user_choice(options)


def _is_quit(user_input: str) -> bool:
    """
    Check whether the user input a quit command.
    """
    return user_input.lower() == 'q'


def _handle_quit() -> tuple[str, str]:
    """
    Handle quit command.
    """
    quit_message = f"\nQuitting the game."
    print(quit_message)
    return 'q', "quit"


def _validate_selection(
        user_input: str, options: dict
):
    """
    Validate the user's selection.
    """
    if not user_input:
        return None

    try:
        selection = int(user_input)
        is_valid_selection = 1 <= selection <= len(options)
        if is_valid_selection:
            option = options.get(selection)
            return selection, option
    except ValueError:
        pass


def _get_user_input(prompt: str = '') -> str:
    """
   Prompt the user for input and return the stripped string.

   Displays the provided prompt and strips any leading and trailing
   whitespace from the input to ensure clean handling.

   Args:
       prompt (str): The message displayed to the user before input.
                     Defaults to an empty string.

   Returns:
       str: The user's input with leading and trailing whitespace removed.
   """

    return input(prompt).strip()


def _prompt_user_choice(options: dict):
    """
    Display available options to the user for selection.
    """
    formatted_options = [f"{key}: {value}" for key, value in options.items()]
    print(f"\nPlease choose a move from:\n{"\n".join(formatted_options)}")
