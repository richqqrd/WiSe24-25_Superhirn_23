# src/CLI/menu_renderer/menu_renderer.py
class MenuRenderer:
    """
    Responsible for rendering the menu
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

    def display_role_menu(self) -> None:
        """
        Displays the role selection menu.
        """
        print("Select your role:")
        print("1. Guesser")
        print("2. Coder")

    def display_languages(self) -> None:
        """
        Displays the language selection menu.
        """
        print("Select a language:")
        print("1. German")
        print("2. English")

    def display_end_game(self) -> None:
        """
        Displays the end game message.
        """
        print("Game ended.")

    def display_save_game(self) -> None:
        """
        Displays the save game message.
        """
        print("Game saved.")

    def display_resume_game(self) -> None:
        """
        Displays the resume game message.
        """
        print("loads resumed game")

    def display_start_game(self) -> None:
        """
        Displays the start game message.
        """
        print("Game started.")
