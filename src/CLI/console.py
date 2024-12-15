from src.BusinessLogic.IBusinessLogic import IBusinessLogic
from src.CLI.game_renderer.game_renderer import GameRenderer
from src.CLI.input_handler.input_handler import InputHandler
from src.CLI.menu_renderer.menu_renderer import MenuRenderer
from src.BusinessLogic.BusinessLogic import BusinessLogic
from src.GameLogic import IGameLogic


class Console:
    """
    Represents a console-based user interface.

    This class handles the interaction with the user via the console,
    relying on an InputHandler to process user inputs.
    """

    def __init__(self,business_logic: IBusinessLogic):
        """
        Initializes the Console instance.

        Args:
            inputHandler (InputHandler): An instance responsible
            for handling user input.
        """
        self.inputHandler = InputHandler()
        self.menuRenderer = MenuRenderer()
        self.game_renderer = GameRenderer()
        self.businessLogic = business_logic

    def run(self) -> None:
        """
        Starts the main loop for the console interface.

        Continuously prompts the user for input,
        processes the input using the InputHandler,
        and prints the result to the console.
        """
        while True:
            self.menuRenderer.display_menu()
            user_input = self.inputHandler.handle_menu_input()
            next_action = self.businessLogic.handle(user_input)

            if next_action == "choose_role":
                self.menuRenderer.display_role_menu()
                role_input = self.inputHandler.handle_role_input()
                next_action = self.businessLogic.handle_role_choice(role_input, "offline")

                if next_action == "need_code_input":
                    self.menuRenderer.display_code_input()
                    code_input = self.inputHandler.handle_code_input()
                    next_action = self.businessLogic.handle_code_input(code_input)

                    if  next_action == "wait_for_computer_guess":
                        next_action = self.businessLogic.handle_computer_guess()
                        game_state = self.businessLogic.get_game_state()
                        self.game_renderer.render_game_state(game_state)

            elif next_action == "choose_role_online":
                self.menuRenderer.display_role_menu()
                role_input = self.inputHandler.handle_role_input()
                next_action = self.businessLogic.handle_role_choice(role_input, "online")

            elif next_action == "choose_language":
                self.menuRenderer.display_languages()
                user_input = self.inputHandler.handle_language_input()
                break
            elif next_action == "end_game":
                self.menuRenderer.display_end_game()
                break
            elif next_action == "save_game":
                self.menuRenderer.display_save_game()
                break
            elif next_action == "resume_interrupted_game":
                self.menuRenderer.display_resume_game()
                break
