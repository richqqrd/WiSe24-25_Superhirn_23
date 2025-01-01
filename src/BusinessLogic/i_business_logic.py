from abc import ABC, abstractmethod

class IBusinessLogic(ABC):
    """Interface for business logic layer"""
    
    @abstractmethod
    def handle(self, command: str) -> str:
        """Handle general commands"""
        pass

    @abstractmethod
    def handle_game_configuration(self, player_name: str, positions: str, colors: str, max_attempts: str) -> str:
        """Handle game configuration input"""
        pass

    @abstractmethod
    def process_game_action(self, action: str, user_input: str = None) -> str:
        """Process game actions and return next state"""
        pass

    @abstractmethod
    def handle_guess_input(self, guess_input: str) -> str:
        """Handle player guess input"""
        pass

    @abstractmethod
    def handle_feedback_input(self, feedback: str) -> str:
        """Handle feedback input"""
        pass

    @abstractmethod
    def handle_menu_action(self, action: str) -> str:
        """Handle menu actions"""
        pass

    @abstractmethod
    def get_required_action(self, game_mode: str) -> str:
        """Get next required action for game mode"""
        pass

    @abstractmethod
    def configure_game(self, game_mode: str, config: dict) -> str:
        """Configure game with given settings"""
        pass

    @abstractmethod
    def get_game_state(self):
        """Get current game state"""
        pass

    @abstractmethod
    def save_game(self) -> str:
        """Save current game state"""
        pass

    @abstractmethod
    def load_game(self) -> str:
        """Load saved game state"""
        pass