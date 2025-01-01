"""Root package for the Mastermind game implementation.

This package contains the complete implementation of the Mastermind game,
organized in a layered architecture:

    - CLI: User interface and input/output handling
    - BusinessLogic: Game flow and rules coordination  
    - GameLogic: Core game mechanics and state management
    - Network: Online gameplay functionality
    - Persistence: Save/load game state handling
    - Util: Shared utilities and constants

The package uses dependency injection and interfaces to maintain loose coupling
between layers.
"""