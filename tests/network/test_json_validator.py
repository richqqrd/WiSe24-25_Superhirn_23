"""Test module for JsonValidator."""

import unittest
import os
import json
from src.network.json_validator import JsonValidator


class TestJsonValidator(unittest.TestCase):
    """Test cases for JsonValidator class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.schema_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../src/util/schema.json")
        )
        self.validator = JsonValidator(self.schema_path)

    def test_load_schema_success(self):
        """Test successful schema loading."""
        schema = self.validator._load_schema(self.schema_path)
        self.assertIsInstance(schema, dict)
        self.assertIn("gameid", schema)
        self.assertIn("gamerid", schema)
        self.assertIn("positions", schema)
        self.assertIn("colors", schema)
        self.assertIn("value", schema)

    def test_load_schema_file_not_found(self):
        """Test schema loading with non-existent file."""
        with self.assertRaises(FileNotFoundError):
            self.validator._load_schema("non_existent_file.json")

    def test_load_schema_invalid_json(self):
        """Test loading invalid JSON schema."""
        invalid_schema_path = "invalid_schema.json"
        with open(invalid_schema_path, "w") as f:
            f.write("invalid json content")

        with self.assertRaises(json.JSONDecodeError):
            self.validator._load_schema(invalid_schema_path)

        os.remove(invalid_schema_path)

    def test_validate_valid_json(self):
        """Test validation with valid JSON data."""
        valid_json = {
            "gameid": 0,
            "gamerid": "player1",
            "positions": 5,
            "colors": 8,
            "value": "",
        }
        self.assertTrue(self.validator.validate(valid_json))

    def test_validate_invalid_json_missing_field(self):
        """Test validation with missing required field."""
        invalid_json = {
            "gameid": 0,
            "gamerid": "player1",
            "colors": 8,
            "value": ""
        }
        self.assertFalse(self.validator.validate(invalid_json))

    def test_validate_invalid_json_wrong_type(self):
        """Test validation with wrong field type."""
        invalid_json = {
            "gameid": "not_an_integer",
            "gamerid": "player1",
            "positions": 5,
            "colors": 8,
            "value": "",
        }
        self.assertFalse(self.validator.validate(invalid_json))


    def test_validate_none_input(self):
        """Test validation with None input."""
        self.assertFalse(self.validator.validate(None))

    def test_validate_non_dict_input(self):
        """Test validation with non-dictionary input."""
        self.assertFalse(self.validator.validate([1, 2, 3]))


if __name__ == "__main__":
    unittest.main()