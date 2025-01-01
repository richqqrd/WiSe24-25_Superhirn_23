import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from src.cli.console import Console
from src.business_logic.i_business_logic import IBusinessLogic


class TestConsole(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.mock_business_logic = MagicMock(spec=IBusinessLogic)
        self.console = Console(self.mock_business_logic)

    @patch(
        "builtins.input",
        side_effect=["1", "1", "12345", "887", "887", "12345", "12345"],
    )
    def test_run(self, mock_input):
        """Test the run method to ensure it correctly processes user input."""
        self.mock_business_logic.handle.side_effect = [
            "choose_role",
            "need_code_input",
            "wait_for_computer_guess",
            "need_feedback_input",
            "need_feedback_input",
            "need_code_input",
            "need_guess_input",
        ]
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.console.run()
            self.assertIn("Main Menu", fake_out.getvalue())
            self.assertIn("Select your role:", fake_out.getvalue())
            self.assertIn("1. guesser", fake_out.getvalue())
            self.assertIn("2. coder", fake_out.getvalue())


if __name__ == "__main__":
    unittest.main()
