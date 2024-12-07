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

    def display_menu(self):
        """
        Displays the main menu options.
        """
        print("Main Menu")
        print("1. Start Game")
        print("2. Change Language")
        print("3. End Game")
        print("4. Save Game")
        print("5. Resume Interrupted Game")

    def change_language(self):
        """
        Handles the change language option.
        """
        print("Language changed.")

    def end_game(self):
        """
        Handles the end game option.
        """
        print("Game ended.")

    def save_game(self):
        """
        Handles the save game option.
        """
        print("Game saved.")

    def start_game(self):
        """
        Handles the start game option.
        """
        print("Game started.")

    def resume_interrupted_game(self):
        """
        Handles resuming an interrupted game.
        """
        print("Resumed interrupted game.")