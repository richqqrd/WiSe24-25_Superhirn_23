from src.BusinessLogic.IBusinessLogic import IBusinessLogic


class BusinessLogic(IBusinessLogic):
    """
    Concrete implementation of the IBusinessLogic interface.
    """

    def __init__(self):
        """
        Initializes the BusinessLogic instance.
        """
        self.commands = {
            "1": self.start_offline_game,
            "2": self.start_online_game,
            "3": self.change_language,
            "4": self.end_game,
            "5": self.save_game,
            "6": self.resume_interrupted_game,
        }

    def handle(self, command: str) -> str:
        action = self.commands.get(command)
        if action:
            return action()
        else:
            return "Invalid command."

    def start_offline_game(self) -> str:
        return "choose_role"

    def start_online_game(self) -> str:
        return "choose_role"

    def change_language(self) -> str:
        return "choose_language"

    def end_game(self) -> str:
        return "end_game"

    def save_game(self) -> str:
        return "save_game"

    def resume_interrupted_game(self) -> str:
        return "resume_interrupted_game"

    def start_offline_game_as_guesser(self) -> None:
        print("Game started as Guesser.")

    def start_offline_game_as_coder(self) -> None:
        print("Game started as Coder.")
