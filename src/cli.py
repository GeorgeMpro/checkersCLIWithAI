def get_choice(
        options: list[str]
) -> tuple[str, str] | tuple[int, str]:
    while True:
        user_input_raw = input()
        user_input_stripped = user_input_raw.strip()
        lower = user_input_stripped.lower()
        if lower == 'q':
            print(f"\nExiting the game.")
            return lower, "quit"

        selection = int(user_input_raw)
        if 1 <= selection <= len(options):
            option = options[selection - 1]
            return selection, option
        else:
            print(f"\nPlease choose a move from:\n{"\n".join(options)}")
