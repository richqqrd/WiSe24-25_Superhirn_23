from typing import List

from src.GameLogic.Coder.ICoder import ICoder
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode


class ComputerCoder(ICoder):
    def give_feedback(self) -> List[FeedbackColorCode]:
        pass

    def generate_code(self) -> List[ColorCode]:
        pass