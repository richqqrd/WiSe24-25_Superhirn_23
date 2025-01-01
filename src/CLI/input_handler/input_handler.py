"""Module for handling user input in the game."""

from src.util.translations import translations


class InputHandler:
    """Handles and validates all user input for the game.
    
    This class provides methods to handle different types of user input
    with proper validation and translation support.

    Attributes:
        language: Current language code for translations
    """

    def __init__(self: "InputHandler", language: str = "en") -> None:
        """Initialize the InputHandler.

        Args:
            language: Language code for translations, defaults to 'en'
        """
        self.language = language

    def set_language(self: "InputHandler", language: str) -> None:
        """Set the display language.

        Args:
            language: Language code to switch to ('en', 'de', etc.)
        """
        if language in translations:
            self.language = language

    def handle_user_input(self: "InputHandler", prefix: str) -> str:
        """Handle generic user input with a prefix.

        Args:
            prefix: Text to display before input prompt

        Returns:
            str: User's input
        """
        user_input = input(prefix)
        return user_input

    def handle_menu_input(self: "InputHandler") -> str:
        """Handle main menu selection input.

        Returns:
            str: User's menu choice
        """
        return self.handle_user_input(translations[self.language]["enter_command"])

    def handle_game_mode_input(self: "InputHandler") -> str:
        """Handle game mode selection input.

        Returns:
            str: Selected game mode
        """
        return self.handle_user_input(translations[self.language]["enter_game_mode"])

    def handle_language_input(self: "InputHandler", language: str) -> str:
        """Handle language selection input.

        Args:
            language: Current language code

        Returns:
            str: Selected language code
        """
        language_options = list(translations.keys())

        language_input = self.handle_user_input("Enter language number: ")
        try:
            selected_language = language_options[int(language_input) - 1]
            return selected_language
        except (IndexError, ValueError):
            print("Invalid input. Defaulting to English.")
            return "en"

    def handle_code_input(self: "InputHandler", positions: int) -> str:
        """Handle secret code input.

        Args:
            positions: Number of positions in the code

        Returns:
            str: Input code string
        """
        return self.handle_user_input(
            translations[self.language]["enter_secret_code"].format(positions)
        )

    def handle_guess_input(self: "InputHandler", positions: int) -> str:
        """Handle user input for making a guess.
        
        Args:
            positions: Number of positions in the code
            
        Returns:
            str: The user's guess as a string
        """
        return self.handle_user_input(
            translations[self.language]["enter_guess"].format(positions)
        )

    def handle_feedback_input(self: "InputHandler", positions: int) -> str:
        """Handle user input for providing feedback.
        
        Args:
            positions: Number of positions in the code
            
        Returns:
            str: The feedback as a string (e.g. '887' for two black, one white)
        """
        return self.handle_user_input(
            translations[self.language]["enter_feedback"].format(positions)
        )

    def handle_ip_input(self: "InputHandler") -> str:
        """Handle user input for server IP address.
        
        Returns:
            str: The entered IP address
        """
        return self.handle_user_input(translations[self.language]["enter_server_ip"])

    def handle_port_input(self: "InputHandler") -> str:
        """Handle user input for server port.
        
        Returns:
            str: The entered port number as string
        """
        return self.handle_user_input(translations[self.language]["enter_server_port"])

    def handle_player_name_input(self: "InputHandler") -> str:
        """Handle input for player name.
        
        Returns:
            str: The entered player name
        """
        return self.handle_user_input(translations[self.language]["enter_player_name"])

    def handle_positions_input(self: "InputHandler") -> str:
        """Handle input for number of positions.
        
        Returns:
            str: The entered number of positions
        """
        return self.handle_user_input(translations[self.language]["enter_positions"])

    def handle_colors_input(self: "InputHandler") -> str:
        """Handle input for number of colors.
        
        Returns:
            str: The entered number of colors
        """
        return self.handle_user_input(translations[self.language]["enter_colors"])

    def handle_max_attempts_input(self: "InputHandler") -> str:
        """Handle input for maximum attempts.
        
        Returns:
            str: The entered maximum number of attempts
        """
        return self.handle_user_input(translations[self.language]["enter_max_attempts"])

    def handle_save_warning_input(self: "InputHandler") -> bool:
        """Handle yes/no input for save warning.
        
        Returns:
            bool: True if user confirms save, False otherwise
        """
        while True:
            user_input = self.handle_user_input(
                f"\n1. {translations[self.language]['yes']}\n"
                f"2. {translations[self.language]['no']}\n"
            ).strip()
            if user_input == "1":  # Yes
                return True
            elif user_input == "2":  # No
                return False
