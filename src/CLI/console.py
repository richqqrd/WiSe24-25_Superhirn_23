from src.CLI.input_handler.input_handler import InputHandler

class Console:
    """
    Represents a console-based user interface.

    This class handles the interaction with the user via the console,
    relying on an InputHandler to process user inputs.
    """
    def __init__(self, inputHandler: InputHandler):
        """
        Initializes the Console instance.

        Args:
            inputHandler (InputHandler): An instance responsible for handling user input.
        """
        self.inputHandler = inputHandler

    def run(self):
        """
        Starts the main loop for the console interface.

        Continuously prompts the user for input, processes the input using the InputHandler,
        and prints the result to the console.
        """
        while True:
            user_input = self.inputHandler.handle_user_input("Enter command: ")
            print(user_input)