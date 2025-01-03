"""Module for JSON schema validation."""

import json
import logging
from typing import Dict, Any

from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate


class JsonValidator:
    """JSON schema validator class.

    This class handles validation of JSON data against a predefined schema.

    Attributes:
        schema: The loaded JSON schema used for validation
    """

    def __init__(self: "JsonValidator", schema_path: str) -> None:
        """Initialize the JsonValidator with a schema.

        Args:
            schema_path: Path to the JSON schema file

        Raises:
            FileNotFoundError: If schema file not found
            json.JSONDecodeError: If schema contains invalid JSON
        """
        self.schema = self._load_schema(schema_path)

    def _load_schema(self: "JsonValidator", schema_path: str) -> Dict[str, Any]:
        """Load JSON schema from file.

        Args:
            schema_path: Path to the JSON schema file

        Returns:
            Dict containing the loaded schema

        Raises:
            FileNotFoundError: If schema file not found
            json.JSONDecodeError: If schema contains invalid JSON
        """
        try:
            with open(schema_path) as file:
                schema = json.load(file)
                return schema
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Failed to load schema: {e}")
            raise

    def validate(self: "JsonValidator", data: Dict[str, Any]) -> bool:
        """Validate data against the JSON schema.

        Args:
            data: The JSON data to validate

        Returns:
            bool: True if valid, False otherwise

        Raises:
            ValidationError: If data does not match schema
        """
        try:
            # First check if data is a dictionary
            if not isinstance(data, dict):
                return False

            if not isinstance(data.get("gameid"), int):
                return False
            if not isinstance(data.get("gamerid"), str):
                return False
            if not isinstance(data.get("positions"), int):
                return False
            if not isinstance(data.get("colors"), int):
                return False
            if not isinstance(data.get("value"), str):
                return False

            validate(data, self.schema)
            logging.info("JSON validation successful.")
            return True
        except ValidationError as err:
            logging.error(f"Validation error: {err.message}")
            return False
