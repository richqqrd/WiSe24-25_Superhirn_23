from src.BusinessLogic.IBusinessLogic import IBusinessLogic
from src.GameLogic.IGameLogic import IGameLogic
from src.util.ColorCode import ColorCode


class BusinessLogic(IBusinessLogic):
    """
    Concrete implementation of the IBusinessLogic interface.
    """

    def get_game_state(self):
        return self.game_logic.get_game_state()

    def handle_computer_guess(self) -> str:
        return self.game_logic.make_computer_guess()

    def _is_valid_code(self, code: str) -> bool:
        if len(code) != 5:
            return False
        return all(c in "12345678" for c in code)

    def handle_code_input(self, code_input: str) -> str:
        if not self._is_valid_code(code_input):
            return "need_code_input"
        try:
            code_list = [ColorCode(int(c)) for c in code_input]
            return self.game_logic.set_secret_code(code_list)
        except ValueError:
            return "need_code_input"

    def handle_guess_input(self, guess_input: str) -> str:
        if not self._is_valid_code(guess_input):
            return "need_guess_input"
        return self.game_logic.make_guess(guess_input)

    def handle_role_choice(self, role_input: str, game_mode: str) -> str:
        if role_input not in ["1", "2"]:
            return "Invalid role."

        if game_mode == "offline":
            if role_input == "1":
                return self.game_logic.startgame("guesser")
            elif role_input == "2":
                return self.game_logic.startgame("coder")


        elif(game_mode == "online"):
            if role_input == "1":
                self.start_online_game_as_guesser()
            else:
                self.start_online_game_as_coder()

    def __init__(self, game_logic: IGameLogic):



        """
        Initializes the BusinessLogic instance.
        """
        self.game_logic = game_logic
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
        return "choose_role_online"

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
