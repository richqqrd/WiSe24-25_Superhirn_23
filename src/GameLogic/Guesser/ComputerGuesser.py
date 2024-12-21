from typing import List

from src.GameLogic.Guesser.IGuesser import IGuesser
from src.util.ColorCode import ColorCode


class ComputerGuesser(IGuesser):
    def make_guess(self) -> List[ColorCode]:
        import random

        return [ColorCode(random.randint(1, 8)) for _ in range(5)]
