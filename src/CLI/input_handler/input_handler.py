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

    def handle_code_input(self) -> str:
        """
        Handles input for code generation.
        """
        return self.handle_user_input(translations[self.language]["enter_secret_code"])

    def handle_guess_input(self) -> str:
        """
        Handles input for code guessing.
        """
        return self.handle_user_input(translations[self.language]["enter_guess"])

    def handle_feedback_input(self) -> str:
        """
        Handles input for feedback generation.
        """
        return self.handle_user_input(translations[self.language]["enter_feedback"])
    def handle_ip_input(self) -> str:
        """
        Handles input for server IP.
        """
        return self.handle_user_input("Enter server IP: ")
    def handle_port_input(self) -> str:
        """
        Handles input for server port.
        """
        return self.handle_user_input("Enter server port: ")