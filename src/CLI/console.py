from src.CLI.input_handler.input_handler import InputHandler
from src.CLI.menu_renderer.menu_renderer import MenuRenderer
from src.BusinessLogic.BusinessLogic import BusinessLogic


class Console:
    """
    Represents a console-based user interface.

    This class handles the interaction with the user via the console,
    relying on an InputHandler to process user inputs.
    """

    def __init__(self, inputHandler: InputHandler, menuRenderer: MenuRenderer):
        """
        Initializes the Console instance.

        Args:
            inputHandler (InputHandler): An instance responsible
            for handling user input.
        """
        self.inputHandler = inputHandler
        self.menuRenderer = menuRenderer
        self.businessLogic = BusinessLogic()

    def run(self) -> None:
        """
        Starts the main loop for the console interface.

        Continuously prompts the user for input,
        processes the input using the InputHandler,
        and prints the result to the console.
        """
        while True:
            self.menuRenderer.display_menu()
            user_input = self.inputHandler.handle_user_input("Enter command: ")
            next_action = self.businessLogic.handle(user_input)

            if next_action == "choose_role":
                self.menuRenderer.display_role_menu()
                user_input = self.inputHandler.handle_user_input("Enter command: ")
                break
            elif next_action == "choose_language":
                self.menuRenderer.display_languages()
                user_input = self.inputHandler.handle_user_input("Enter command: ")
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
