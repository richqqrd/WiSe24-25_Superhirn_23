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
    def start_offline_game(self) -> str:
        """
        Start an offline game.
        """
        pass

    @abstractmethod
    def start_offline_game_as_guesser(self) -> str:
        """
        Start an offline game as the guesser.
        """
        pass

    @abstractmethod
    def start_offline_game_as_coder(self) -> str:
        """
        Start an offline game as the coder.
        """
        pass

    @abstractmethod
    def start_online_game(self) -> str:
        """
        Start an online game.
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
    def resume_interrupted_game(self) -> str:
        """
        Resume an interrupted game.
        """
        pass
