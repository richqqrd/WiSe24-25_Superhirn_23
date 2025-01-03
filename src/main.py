"""Main entry point for the Mastermind game application.

This module initializes and starts the game by creating instances of the game logic,
business logic, and user interface components.

The module follows a layered architecture pattern where:
- Console handles user interaction
- business_logic handles game flow control
- game_logic handles core game mechanics
"""

from CLI.console import Console
from business_logic.business_logic import BusinessLogic
from game_logic.game_logic import GameLogic
from src.Persistence.persistence_manager import PersistenceManager


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
    game_logic = GameLogic(persistence_manager)
    business_logic = BusinessLogic(game_logic)
    ui = Console(business_logic)
    ui.run()


if __name__ == "__main__":
    main()
