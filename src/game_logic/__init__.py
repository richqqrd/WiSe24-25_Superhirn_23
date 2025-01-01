"""game_logic package for core game mechanics.

This package implements the core game logic including:
    - game_logic: Main game mechanics implementation
    - GameState: Game state management
    - GameTurn: Turn tracking
    - coder: Code maker implementation (player/computer)
    - guesser: Code breaker implementation (player/computer)

The package follows a layered architecture pattern with clear separation
between game logic and other components.

Dependencies:
    - network: For online gameplay
    - persistence: For save/load functionality
    - Util: For color codes and feedback"""
