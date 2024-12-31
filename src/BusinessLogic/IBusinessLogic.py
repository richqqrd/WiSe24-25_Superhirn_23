from abc import ABC, abstractmethod


class IBusinessLogic(ABC):
    """
    Interface for the business logic related to the game operations.
    """

    @abstractmethod
    def handle(self, command: str) -> str:
        """
        Handles a command string and invokes the corresponding method.

        Args:
            command (str): The command string to process.
        """
        pass


    @abstractmethod
    def change_language(self) -> str:
        """
        Change the language of the game.
        """
        pass

    @abstractmethod
    def end_game(self) -> str:
        """
        End the current game.
        """
        pass

    @abstractmethod
    def save_game(self) -> str:
        """
        Save the current game state.
        """
        pass

    @abstractmethod
    def load_game(self) -> str:
        """
        Resume an interrupted game.
        """
        pass

    @abstractmethod
    def handle_role_choice(self, role_input: str, game_mode: str) -> str:
        """
        Handle the user's role choice for the game.

        Args:
            role_input (str): The role chosen by the user.
            game_mode (str): The game mode selected by the user.
        """
        pass

    @abstractmethod
    def handle_code_input(self, code_input: str) -> str:
        """
        Handle the code input provided by the user.

        Args:
            code_input (str): The code input provided by the user.
        """
        pass

    @abstractmethod
    def handle_guess_input(self, guess_input: str) -> str:
        """
        Handle the guess input provided by the user.

        Args:
            guess_input (str): The guess input provided by the user.
        """
        pass

    @abstractmethod
    def handle_computer_guess(self) -> str:
        """
        Handle the computer's guess in the game.
        """
        pass

    @abstractmethod
    def get_game_state(self):
        """
        Get the current game state.
        """
        pass

    @abstractmethod
    def handle_feedback_input(self, feedback_input: str) -> str:
        """
        Handle the feedback input provided by the user.

        Args:
            feedback_input (str): The feedback input provided by the user.
        """
        pass

    def handle_server_connection(self, server_ip, server_port):
        pass

    def handle_game_mode_choice(self, game_mode):
        pass
