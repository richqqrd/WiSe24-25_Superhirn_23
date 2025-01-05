"""Unit tests for the main module of the Mastermind game application."""

import unittest
from unittest.mock import patch, MagicMock


class TestMain(unittest.TestCase):
    """Test case for the main function in the Mastermind game application."""

    @patch('src.main.PersistenceManager')
    @patch('src.main.BusinessLogic')
    @patch('src.main.ApplicationLogic')
    @patch('src.main.Console')
    def test_main(self: "TestMain", mock_console: MagicMock,
                  mock_application_logic: MagicMock,
                  mock_business_logic: MagicMock,
                  mock_persistence_manager: MagicMock) -> None:
        """Test that the main function creates the necessary instances.

        Calls the run method.
        """
        # Mock instances
        mock_persistence_instance = MagicMock()
        mock_business_instance = MagicMock()
        mock_application_instance = MagicMock()
        mock_console_instance = MagicMock()

        # Set return values for the constructors
        mock_persistence_manager.return_value = mock_persistence_instance
        mock_business_logic.return_value = mock_business_instance
        mock_application_logic.return_value = mock_application_instance
        mock_console.return_value = mock_console_instance

        # Import the main function and call it
        from src.main import main
        main()

        # Verify that the instances were created and methods called
        mock_persistence_manager.assert_called_once()
        mock_business_logic.assert_called_once_with(mock_persistence_instance)
        mock_application_logic.assert_called_once_with(mock_business_instance)
        mock_console.assert_called_once_with(mock_application_instance)
        mock_console_instance.run.assert_called_once()


if __name__ == "__main__":
    unittest.main()
