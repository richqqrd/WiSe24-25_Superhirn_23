from typing import List

from src.GameLogic.Guesser.IGuesser import IGuesser
from src.util.ColorCode import ColorCode


class PlayerGuesser(IGuesser):
    def __init__(self):
        self.current_guess: List[ColorCode] = []

    def make_guess(self) -> List[ColorCode]:
        return self.current_guess

    def set_guess(self, guess: List[ColorCode]):
        self.current_guess = guess
