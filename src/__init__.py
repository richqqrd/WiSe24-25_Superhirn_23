"""Root package for the Mastermind game implementation.

This package contains the complete implementation of the Mastermind game,
organized in a layered architecture:

    - cli: User interface and input/output handling
    - application_logic: Game flow and rules coordination
    - business_logic: Core game mechanics and state management
    - network: Online gameplay functionality
    - persistence: Save/load game state handling
    - Util: Shared utilities and constants

The package uses dependency injection and interfaces to maintain loose coupling
between layers."""
