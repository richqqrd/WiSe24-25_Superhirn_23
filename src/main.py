"""Main entry point for the Mastermind game application.

This module initializes and starts the game by creating instances of the game logic,
business logic, and user interface components.

The module follows a layered architecture pattern where:
- Console handles user interaction
- business_logic handles game flow control
- game_logic handles core game mechanics
"""

from cli.console import Console
from src.application_logic.application_logic import ApplicationLogic
from src.business_logic.business_logic import BusinessLogic
from src.persistence.persistence_manager import PersistenceManager


def main() -> None:
    """Initialize and start the Mastermind game application.

    Creates instances of:
        - PersistenceManager for save/load functionality
        - game_logic for core game mechanics
        - business_logic for game flow control
        - Console for user interface

    Then starts the main game loop through the Console.
    """
    persistence_manager = PersistenceManager()
    business_logic = BusinessLogic(persistence_manager)
    application_logic = ApplicationLogic(business_logic)
    ui = Console(application_logic)
    ui.run()


if __name__ == "__main__":
    main()
