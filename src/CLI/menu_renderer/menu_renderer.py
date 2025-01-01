"""Module for rendering game menus."""

from src.util.color_code import ColorCode
from src.util.translations import translations


class MenuRenderer:
    """Renders game menus and user interface elements.
    
    This class is responsible for displaying various menus and UI elements
    with proper translation support.
    
    Attributes:
        language: Current language code for translations
    """

    def __init__(self: "MenuRenderer", language: str = "en") -> None:
        """Initialize the MenuRenderer.

        Args:
            language: Language code for translations, defaults to 'en'
        """
        self.language = language

    def set_language(self: "MenuRenderer", language: str) -> None:
        """Set the display language.

        Args:
            language: Language code to switch to ('en', 'de', etc.)
        """
        if language in translations:
            self.language = language

    def display_main_menu(self: "MenuRenderer") -> None:
        """Display the main menu options.
        
        Shows translated menu items:
            1. Start Game
            2. Change Language  
            3. Resume Game
            4. End Game
        """
        print(translations[self.language]["main_menu"])
        print(f"1. {translations[self.language]['start_game']}")
        print(f"2. {translations[self.language]['change_language']}")
        print(f"3. {translations[self.language]['resume_game']}")
        print(f"4. {translations[self.language]['end_game']}")

    def display_ingame_menu(self: "MenuRenderer", available_actions: list) -> None:
        """Display the in-game menu options.
        
        Shows different menu items based on available actions.

        Args:
            available_actions: List of allowed menu actions
        """
        print(translations[self.language]["ingame_menu"])
        menu_items = []
        if "save_game" in available_actions:
            menu_items.append((1, translations[self.language]["save_game"]))
            menu_items.append((2, translations[self.language]["change_language"]))
            menu_items.append((3, translations[self.language]["resume_game"]))
            menu_items.append((4, translations[self.language]["end_game"]))
        else:
            menu_items.append((1, translations[self.language]["change_language"]))
            menu_items.append((2, translations[self.language]["end_game"]))

        for number, text in menu_items:
            print(f"{number}. {text}")

    def display_game_mode_menu(self: "MenuRenderer") -> None:
        """Display the game mode selection menu.
        
        Shows translated menu items:
            1. Play as Guesser (offline)
            2. Play as Coder (offline)  
            3. Play as Guesser (online)
            4. Back to Main Menu
        """
        print(translations[self.language]["select_game_mode"])
        print(f"1. {translations[self.language]['offline_guesser']}")
        print(f"2. {translations[self.language]['offline_coder']}")
        print(f"3. {translations[self.language]['online_guesser']}")
        print(f"4. {translations[self.language]['back_to_menu']}")

    def display_languages(self: "MenuRenderer") -> None:
        """Display the language selection menu.
        
        Shows available languages with their translated names.
        Languages are numbered starting from 1.
        """
        print(translations[self.language]["select_language"])
        for index, lang in enumerate(translations.keys(), 1):
            print(f"{index}. {translations[self.language]['language_' + lang]}")

    def display_end_game(self: "MenuRenderer") -> None:
        """Display game end message.
        
        Shows translated message when game ends.
        """
        print(translations[self.language]["game_ended"])

    def display_save_game(self: "MenuRenderer") -> None:
        """Display game save message.
        
        Shows translated confirmation when game is saved.
        """
        print(translations[self.language]["game_saved"])

    def display_load_game(self: "MenuRenderer") -> None:
        """Display message when loading a saved game.
        
        Shows translated message confirming game load operation.
        """
        print(translations[self.language]["loads_resumed_game"])

    def display_start_game(self: "MenuRenderer") -> None:
        """Display game start message.
        
        Shows translated message when new game starts.
        """
        print(translations[self.language]["game_started"])

    def display_code_input(self: "MenuRenderer", available_colors: int) -> None:
        """Display color selection for code input.
    
        Shows available colors and their codes up to the specified limit.
        
        Args:
            available_colors: Maximum number of colors to display
        """
        print(f"\n{translations[self.language]['available_colors']}")
        for color in list(ColorCode)[:available_colors]:
            print(f"{color.value}: {color}")

    def display_guess_input(self: "MenuRenderer") -> None:
        """Display available colors for making a guess.
        
        Shows all available colors and their corresponding codes.
        """
        print(f"\n{translations[self.language]['available_colors']}")
        for color in ColorCode:
            print(f"{color.value} : {color}")

    def display_feedback_input(self: "MenuRenderer") -> None:
        """Display feedback input instructions.
        
        Shows instructions for providing feedback using black/white pins.
        """
        print(f"\n{translations[self.language]['give_feedback']}")
        print(translations[self.language]["feedback_instructions"])

    def display_server_connection(self: "MenuRenderer") -> None:
        """Display server connection input prompts.
        
        Shows translated prompts for server IP and port input.
        """
        print(f"\n{translations[self.language]['enter_server_ip']}")
        print(f"{translations[self.language]['enter_server_port']}")

    def display_cheating_warning(self: "MenuRenderer") -> None:
        """Display warning when cheating is detected.
        
        Shows translated warning message about detected cheating.
        """
        print(translations[self.language]["cheating_warning"])

    def display_player_name_input(self: "MenuRenderer") -> None:
        """Display player name input prompt.
        
        Shows translated prompt for entering player name.
        """
        print(translations[self.language]["pick_player_name"])

    def display_positions_input(self: "MenuRenderer") -> None:
        """Display positions input prompt.
        
        Shows translated prompt for entering number of code positions.
        """
        print(translations[self.language]["pick_positions"])

    def display_colors_input(self: "MenuRenderer") -> None:
        """Display colors input prompt.
        
        Shows translated prompt for entering number of colors.
        """
        print(translations[self.language]["pick_colors"])

    def display_max_attempts_input(self: "MenuRenderer") -> None:
        """Display maximum attempts input prompt.
        
        Shows translated prompt for entering maximum allowed attempts.
        """
        print(translations[self.language]["pick_max_attempts"])

    def display_save_warning(self: "MenuRenderer") -> None:
        """Display warning about overwriting existing save.
        
        Shows translated warning message and yes/no options for confirmation
        when attempting to save over an existing save file.
        """
        print(translations[self.language]["save_warning"])
        print(f"1. {translations[self.language]['yes']}")
        print(f"2. {translations[self.language]['no']}")

    def display_color_selection(self: "MenuRenderer") -> None:
        """Display available colors for selection.
        
        Shows all available colors with their codes and values,
        followed by color input prompt.
        """
        print(f"\n{translations[self.language]['available_colors']}")
        for color in ColorCode:
            print(f"{color.value} : {color}")
        print(f"\n{translations[self.language]['enter_colors']}")

    def display_feedback_instructions(self: "MenuRenderer") -> None:
        """Display instructions for providing feedback.
        
        Shows translated instructions for how to input feedback
        using black and white pins.
        """
        print(f"\n{translations[self.language]['feedback_instructions']}")

    def display_invalid_configuration(self: "MenuRenderer") -> None:
        """Display invalid configuration error message.
        
        Shows translated error message when game settings are invalid.
        """
        print(f"\n{translations[self.language]['invalid_configuration']}")

    def display_game_won(self: "MenuRenderer") -> None:
        """Display game won message.
        
        Shows translated victory message when player wins the game.
        """
        print(translations[self.language]["game_won"])

    def display_game_lost(self: "MenuRenderer") -> None:
        """Display game lost message.
        
        Shows translated defeat message when player loses the game.
        """
        print(translations[self.language]["game_lost"])
