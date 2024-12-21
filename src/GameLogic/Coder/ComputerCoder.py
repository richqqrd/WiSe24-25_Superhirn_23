import random
from typing import List

from src.GameLogic.Coder.ICoder import ICoder
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode


class ComputerCoder(ICoder):

    def __init__(self):
        self.__secret_code = []

    def give_feedback(self, guess: List[ColorCode]) -> List[FeedbackColorCode]:
        feedback = []

        if len(guess) != len(self.secret_code):
            return feedback

        secret_code = self.secret_code.copy()
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
        self.secret_code = [ColorCode(random.randint(1, 8)) for _ in range(5)]
        return self.secret_code