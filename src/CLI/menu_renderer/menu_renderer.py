# src/CLI/menu_renderer/menu_renderer.py
from src.util.ColorCode import ColorCode


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

    def display_code_input(self) -> None:
        """
        Displays the available colors and their codes.
        """
        print("\nAvailable colors and their codes:")
        for color in ColorCode:
            print(f"{color.value} : {color}")

    def display_guess_input(self) -> None:
        """
        Displays the available colors and their codes.
        """
        print("\nAvailable colors and their codes:")
        for color in ColorCode:
            print(f"{color.value} : {color}")

    def display_feedback_input(self) -> None:
        print("\nGive feedback for the guess:")
        print("8: Black (correct color in correct position)")
        print("7: White (correct color in wrong position)")
        print("Enter feedback (e.g. 887 for two black, one white):")