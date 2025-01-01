"""Main entry point for the Mastermind game application.

This module initializes and starts the game by creating instances of the game logic,
business logic, and user interface components.

The module follows a layered architecture pattern where:
- Console handles user interaction
- BusinessLogic handles game flow control
- GameLogic handles core game mechanics
"""

from CLI.console import Console
from BusinessLogic.business_logic import BusinessLogic
from GameLogic.game_logic import GameLogic
from src.Persistence.persistence_manager import PersistenceManager


def main() -> None:
    """Initialize and start the Mastermind game application.

    Creates instances of:
        - PersistenceManager for save/load functionality
        - GameLogic for core game mechanics
        - BusinessLogic for game flow control
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
