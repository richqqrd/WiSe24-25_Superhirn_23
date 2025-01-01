import json
import logging
from typing import Dict, Any

from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate


class JsonValidator:
    def __init__(self, schema_path: str):
        """
        Initialize the JsonValidator with the path to the JSON schema.

        Args:
            schema_path (str): The file path to the JSON schema.
        """
        self.schema = self._load_schema(schema_path)

    def _load_schema(self, schema_path: str) -> Dict[str, Any]:
        """
        Load the JSON schema from the specified file path.

        Args:
            schema_path (str): The file path to the JSON schema.

        Returns:
            Dict[str, Any]: The loaded JSON schema.

        Raises:
            FileNotFoundError: If the schema file is not found.
            json.JSONDecodeError: If the schema file contains invalid JSON.
        """
        try:
            with open(schema_path) as file:
                schema = json.load(file)
                return schema
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Failed to load schema: {e}")
            raise

    def validate(self, data: Dict[str, Any]) -> bool:
        """
        Validate the given data against the loaded JSON schema.

        Args:
            data (Dict[str, Any]): The JSON data to validate.

        Returns:
            bool: True if the data is valid, False otherwise.

        Raises:
            ValidationError: If the data does not conform to the schema.
        """
        try:

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
