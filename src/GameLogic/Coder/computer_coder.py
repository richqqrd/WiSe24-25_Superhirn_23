import random
from typing import List

from src.GameLogic.Coder.i_coder import ICoder
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


class ComputerCoder(ICoder):

    def __init__(self, positions: int, colors: int):
        self.__secret_code = []
        self.positions = positions
        self.colors = colors

    def give_feedback(self, guess: List[ColorCode]) -> List[FeedbackColorCode]:
        feedback = []

        if len(guess) != self.positions:
            return feedback

        secret_code = self.__secret_code.copy()
        guess_code = guess.copy()

        for i in range(len(secret_code)):
            if guess_code[i] == secret_code[i]:
                feedback.append(FeedbackColorCode.BLACK)
                secret_code[i] = None
                guess_code[i] = None

        for i in range(len(guess_code)):
            if guess_code[i] is not None:
                if guess_code[i] in secret_code:
                    feedback.append(FeedbackColorCode.WHITE)
                    secret_code[secret_code.index(guess_code[i])] = None

        return feedback

    def generate_code(self) -> List[ColorCode]:
        self.__secret_code = [
            ColorCode(random.randint(1, self.colors)) for _ in range(self.positions)
        ]
        return self.__secret_code

    @property
    def secret_code(self) -> List[ColorCode]:
        """Get the secret code"""
        return self.__secret_code

    @secret_code.setter
    def secret_code(self, code: List[ColorCode]):
        """Set the secret code"""
        self.__secret_code = code
