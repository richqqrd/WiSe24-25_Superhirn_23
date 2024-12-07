from CLI.console import Console
from CLI.input_handler.input_handler import InputHandler


def main():
    """
    Entry point for the application.

    Creates an instance of the user interface (Console),
    linked with an InputHandler to process inputs,
    and starts the application's main runtime loop.
    """
    ui = Console(InputHandler())
    ui.run()


if __name__ == "__main__":
    """
    Main program execution.

    Executes the main function if the file is run directly.
    """
    main()
