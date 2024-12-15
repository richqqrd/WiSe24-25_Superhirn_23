from typing import List

from src.GameLogic.Coder.ICoder import ICoder
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode


class PlayerCoder(ICoder):
    def __init__(self):
        self.code: List[ColorCode] = []


    def generate_code(self) -> List[ColorCode]:
        if not self.code:
            raise ValueError("Code is not set")
        return self.code

    def give_feedback(self) -> List[FeedbackColorCode]:
        pass
