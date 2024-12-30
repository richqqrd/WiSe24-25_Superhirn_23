from src.util.ColorCode import ColorCode
from src.util.translations import translations

class MenuRenderer:
    """
    Responsible for rendering the menu
    """

    def __init__(self, language: str = "en"):
        """
        Initializes the MenuRenderer.
        """
        self.language = language

    def set_language(self, language: str) -> None:
        """
        Sets the language for the menu.

        :param language: The language code (e.g., 'en' or 'de').
        """
        if language in translations:
            self.language = language

    def display_menu(self) -> None:
        """
        Displays the main menu options.
        """
        print(translations[self.language]["main_menu"])
        print(translations[self.language]["start_offline_game"])
        print(translations[self.language]["start_online_game"])
        print(translations[self.language]["change_language"])
        print(translations[self.language]["end_game"])
        print(translations[self.language]["save_game"])
        print(translations[self.language]["resume_game"])

    def display_role_menu(self) -> None:
        """
        Displays the role selection menu.
        """
        print(translations[self.language]["select_role"])
        print(translations[self.language]["guesser"])
        print(translations[self.language]["coder"])

    def display_languages(self) -> None:
        """
        Displays the language selection menu dynamically.
        """
        print(translations[self.language]["select_language"])
        for index, lang in enumerate(translations.keys(), 1):
            print(f"{index}. {translations[self.language]['language_' + lang]}")

    def display_end_game(self) -> None:
        """
        Displays the end game message.
        """
        print(translations[self.language]["game_ended"])

    def display_save_game(self) -> None:
        """
        Displays the save game message.
        """
        print(translations[self.language]["game_saved"])

    def display_resume_game(self) -> None:
        """
        Displays the resume game message.
        """
        print(translations[self.language]["loads_resumed_game"])

    def display_start_game(self) -> None:
        """
        Displays the start game message.
        """
        print(translations[self.language]["game_started"])

    def display_code_input(self) -> None:
        """
        Displays the available colors and their codes.
        """
        print(f"\n{translations[self.language]['available_colors']}")
        for color in ColorCode:
            print(f"{color.value} : {color}")

    def display_guess_input(self) -> None:
        """
        Displays the available colors and their codes.
        """
        print(f"\n{translations[self.language]['available_colors']}")
        for color in ColorCode:
            print(f"{color.value} : {color}")

    def display_feedback_input(self) -> None:
        """
        Displays the feedback input options.
        """
        print(f"\n{translations[self.language]['give_feedback']}")
        print(translations[self.language]["feedback_instructions"])
    def display_server_connection(self) -> None:
        """
        Displays the server connection input options.
        """
        print(f"\n{translations[self.language]['enter_server_ip']}")
        print(f"{translations[self.language]['enter_server_port']}")