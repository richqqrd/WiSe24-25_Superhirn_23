from typing import List

from src.GameLogic.Guesser.IGuesser import IGuesser
from src.util.ColorCode import ColorCode


class PlayerGuesser(IGuesser):
    def make_guess(self) -> List[ColorCode]:
        pass