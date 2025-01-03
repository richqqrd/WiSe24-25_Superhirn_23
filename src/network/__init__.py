"""network package for handling online gameplay functionality.

This package provides network communication capabilities for online gameplay:
    - NetworkService: Handles game server communication
    - HTTPHandler: Manages HTTP requests
    - HTTPClient: Low-level HTTP client
    - JsonValidator: Validates JSON data against schema
    - INetworkService: Interface defining network operations

The package follows the layered architecture pattern and uses
dependency injection for loose coupling.

Dependencies:
    - requests: For HTTP communication
    - jsonschema: For JSON validation
"""
