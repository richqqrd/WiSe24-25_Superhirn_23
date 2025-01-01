import unittest
import os
from src.Network.json_validator import JsonValidator


class TestJsonValidator(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case with an instance of JsonValidator.
        """
        self.schema_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../src/util/schema.json")
        )
        self.validator = JsonValidator(self.schema_path)

    def test_load_schema_success(self):
        """
        Test successful schema loading.
        """
        schema = self.validator._load_schema(self.schema_path)
        self.assertIsInstance(schema, dict)
        self.assertIn("gameid", schema)
        self.assertIn("gamerid", schema)
        self.assertIn("positions", schema)
        self.assertIn("colors", schema)
        self.assertIn("value", schema)

    def test_load_schema_file_not_found(self):
        """
        Test schema loading with non-existent file.
        """
        with self.assertRaises(FileNotFoundError):
            self.validator._load_schema("non_existent_file.json")

    def test_validate_valid_json(self):
        """
        Test validation with valid JSON data.
        """
        valid_json = {
            "gameid": 0,
            "gamerid": "player1",
            "positions": 5,
            "colors": 8,
            "value": "",
        }
        self.assertTrue(self.validator.validate(valid_json))

    def test_validate_invalid_json_missing_field(self):
        """
        Test validation with missing required field.
        """
        invalid_json = {"gameid": 0, "gamerid": "player1", "colors": 8, "value": ""}
        self.assertFalse(self.validator.validate(invalid_json))

    def test_validate_invalid_json_wrong_type(self):
        """
        Test validation with wrong field type.
        """
        invalid_json = {
            "gameid": "not_an_integer",
            "gamerid": "player1",
            "positions": 5,
            "colors": 8,
            "value": "",
        }
        self.assertFalse(self.validator.validate(invalid_json))

    def test_validate_invalid_json_extra_field(self):
        """
        Test validation with extra field.
        """
        invalid_json = {
            "gameid": 0,
            "gamerid": "player1",
            "positions": 5,
            "colors": 8,
            "value": "",
            "extra_field": "should not be here",
        }
        self.assertTrue(self.validator.validate(invalid_json))


if __name__ == "__main__":
    unittest.main()
