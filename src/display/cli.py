import re

from state.move_state import MoveState


def extract_move_chosen_by_user(
        moves_to_dict: dict[int, str]
) -> tuple[str, str]:
    """
   Extracts the source and target positions from the move chosen by the user.

   Parameters:
   - selection: The user's choice (e.g., a key or index).
   - moves_to_dict: Dictionary of available moves, mapping choices to move strings.

   Returns:
   """
    selection, option = get_choice(moves_to_dict)
    if selection == "q":
        return selection, option

    chosen_move = moves_to_dict.get(selection)
    src_actual, tar_actual = extract_src_target_names(chosen_move)
    return src_actual, tar_actual


def get_choice(options: dict) -> tuple[str, str] | tuple[int, str]:
    """
    Prompt the user for input and validate it against available options.

     Returns:
        tuple[str, str]: If the user chooses to quit.
        tuple[int, str]: A tuple with the move index and the corresponding move description
                         if a valid move is selected.
    """
    # todo
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
    print("press 'q' to quit")


def moves_dto_to_dict(
        moves: list[MoveState]
) -> dict:
    """
    Transform available moves into a dictionary.
    """
    moves_to_dict = {
        idx + 1: f"{move.src_name} -> {target}"
        for idx, (move, target) in enumerate(
            (move, target) for move in moves for target in move.target_names
        )
    }
    return moves_to_dict


def parse_prompt(prompt: str) -> dict[int, str]:
    """Transforms prompt text into a dictionary similar to moves_to_dict."""
    parsed_result = {}
    for line in prompt.strip().splitlines():
        match = re.match(r'\[(\d+)]\s*(\S+\s*->\s*\S+)', line)
        if match:
            move_number = int(match.group(1))  # Extract the index
            move_text = match.group(2).strip()  # Extract the move
            parsed_result[move_number] = move_text
    return parsed_result


def extract_src_target_names(chosen_move: str) -> tuple[str, str]:
    """
        Extracts the source and target cell positions from selected move.

        Parameters:
        - chosen_move (str): A string representing a move in the format "a_ij -> a_kl"
                             or "a_ij -> a_kl -> a_uv" (for captures).

        Returns:
        - tuple[str, str]: A tuple containing the source cell (src) and target cell (tar).

        Example:
        >>> extract_src_target_names("a13 -> a24")
        ('a13', 'a24')

        >>> extract_src_target_names("a13 -> a24 -> a45")
        ('a13', 'a24')

        Notes:
        - Assumes that the input string is in a correct format and that the first two
          positions represent the initial and target cells for the move.
        - Ignores any additional cells beyond the first two, focusing only on src and tar.
        """
    # Use regex to find all `a_ij` patterns
    matches = re.findall(r'a\d+', chosen_move)
    src, tar = matches[:2]
    return src, tar
