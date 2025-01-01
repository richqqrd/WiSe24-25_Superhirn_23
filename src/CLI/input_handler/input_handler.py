from src.util.translations import translations


class InputHandler:

    def __init__(self, language: str = "en"):
        """
        Initializes the GameRenderer.
        """
        self.language = language

    def set_language(self, language: str) -> None:
        """
        Sets the language for the game renderer.
        """
        if language in translations:
            self.language = language

    def handle_user_input(self, prefix: str):
        user_input = input(prefix)
        return user_input

    def handle_menu_input(self) -> str:
        """
        Handles input for the main menu (1-6).
        """
        return self.handle_user_input(translations[self.language]["enter_command"])

    def handle_game_mode_input(self) -> str:
        """
        Handles input for game mode selection (1-2).
        """
        return self.handle_user_input(translations[self.language]["enter_game_mode"])

    def handle_language_input(self, language: str) -> str:
        """
        Handles input for language selection based on available translations.
        """
        language_options = list(translations.keys())

        language_input = self.handle_user_input("Enter language number: ")
        try:
            selected_language = language_options[int(language_input) - 1]
            return selected_language
        except (IndexError, ValueError):
            print("Invalid input. Defaulting to English.")
            return "en"

    def handle_code_input(self, positions: int) -> str:
        """
        Handles input for code generation.
        """
        return self.handle_user_input(
            translations[self.language]["enter_secret_code"].format(positions)
        )
    def handle_guess_input(self, positions: int) -> str:
        """
        Handles input for code guessing.
        """
        return self.handle_user_input(
            translations[self.language]["enter_guess"].format(positions))

    def handle_feedback_input(self, positions: int) -> str:
        """
        Handles input for feedback generation.
        """
        return self.handle_user_input(
            translations[self.language]["enter_feedback"].format(positions)
        )

    def handle_ip_input(self) -> str:
        """
        Handles input for server IP.
        """
        return self.handle_user_input(translations[self.language]["enter_server_ip"])

    def handle_port_input(self) -> str:
        """
        Handles input for server port.
        """
        return self.handle_user_input(translations[self.language]["enter_server_port"])

    def handle_player_name_input(self) -> str:
        """
        Handles input for player name.
        """
        return self.handle_user_input(translations[self.language]["enter_player_name"])

    def handle_positions_input(self) -> str:
        """
        Handles input for positions.
        """
        return self.handle_user_input(translations[self.language]["enter_positions"])

    def handle_colors_input(self) -> str:
        """
        Handles input for colors.
        """
        return self.handle_user_input(translations[self.language]["enter_colors"])

    def handle_max_attempts_input(self) -> str:
        """
        Handles input for max attempts.
        """
        return self.handle_user_input(translations[self.language]["enter_max_attempts"])

    def handle_save_warning_input(self) -> bool:
        """Handle yes/no input for save warning"""
        while True:
            user_input = self.handle_user_input(f"\n1. {translations[self.language]['yes']}\n"
                               f"2. {translations[self.language]['no']}\n").strip()
            if user_input == "1":  # Yes
                return True
            elif user_input == "2":  # No
                return False