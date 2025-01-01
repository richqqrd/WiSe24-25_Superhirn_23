from CLI.console import Console
from BusinessLogic.BusinessLogic import BusinessLogic
from GameLogic.GameLogic import GameLogic
from src.BusinessLogic.IBusinessLogic import IBusinessLogic
from src.Persistence.PersistenceManager import PersistenceManager


def main():
    """
    Entry point for the application.

    Creates an instance of the user interface (Console),
    linked with an InputHandler to process inputs,
    and starts the application's main runtime loop.
    """
    persistence_manager = PersistenceManager()
    game_logic = GameLogic(persistence_manager)
    business_logic = BusinessLogic(game_logic)
    ui = Console(business_logic)
    ui.run()


if __name__ == "__main__":
    """
    Main program execution.

    Executes the main function if the file is run directly.
    """
    main()
