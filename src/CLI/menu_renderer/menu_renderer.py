# src/CLI/menu_renderer/menu_renderer.py
class MenuRenderer:
    """
    Responsible for rendering the menu and handling menu options.
    """

    def __init__(self):
        """
        Initializes the MenuRenderer.
        """
        pass

    def display_menu(self) -> None:
        """
        Displays the main menu options.
        """
        print("Main Menu")
        print("1. Start Offline Game")
        print("2. Start Online Game")
        print("3. Change Language")
        print("4. End Game")
        print("5. Save Game")
        print("6. Resume Interrupted Game")



    def start_offline_game(self) -> None:
        """
        Handles the start game option.
        """
        print("1. Play as Guesser")
        print("2. Play as Coder")

    def start_offline_game_as_guesser(self) -> None:
        print("Game started as Guesser.")

    def start_offline_game_as_coder(self) -> None:
        print("Game started as Coder.")

    def start_online_game(self) -> None:
        """
        Handles the start online game option.
        :return:
        """
        print("Game started.")

    def change_language(self) -> None:
        """
        Handles the change language option.
        """
        print("Language changed.")

    def end_game(self) -> None:
        """
        Handles the end game option.
        """
        print("Game ended.")

    def save_game(self) -> None:
        """
        Handles the save game option.
        """
        print("Game saved.")

    def resume_interrupted_game(self) -> None:
        """
        Handles resuming an interrupted game.
        """
        print("Resumed interrupted game.")
