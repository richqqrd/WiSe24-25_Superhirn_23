"""GameLogic package for core game mechanics.

This package implements the core game logic including:
    - GameLogic: Main game mechanics implementation
    - GameState: Game state management
    - GameTurn: Turn tracking
    - Coder: Code maker implementation (player/computer)
    - Guesser: Code breaker implementation (player/computer)

The package follows a layered architecture pattern with clear separation
between game logic and other components.

Dependencies:
    - Network: For online gameplay
    - Persistence: For save/load functionality 
    - Util: For color codes and feedback
"""