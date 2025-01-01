"""Persistence package for managing game state storage.

This package provides functionality for saving and loading game states:
    - PersistenceManager: Handles saving/loading game states to/from files
    - IPersistenceManager: Interface defining persistence operations

The persistence layer uses pickle for serialization and follows the
layered architecture pattern.
"""