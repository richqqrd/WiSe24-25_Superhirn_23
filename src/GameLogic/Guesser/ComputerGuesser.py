from itertools import product
from typing import List, Set
from src.GameLogic.Guesser.IGuesser import IGuesser
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode


class ComputerGuesser(IGuesser):
    def __init__(self):
        self.possible_codes = self._generate_all_possible_codes()
        self.last_guess = None
        self.first_guess = True

    def _generate_all_possible_codes(self) -> Set[tuple]:
        """
        Generate all possible codes.

        Returns:
            Set[tuple]: A set of all possible color code combinations.
        """
        colors = [ColorCode(i) for i in range(1, 9)]
        return set(product(colors, repeat=5))

    def make_guess(self) -> List[ColorCode]:
        """
        Make a guess for the secret code.

        Returns:
            List[ColorCode]: The guessed color code.
        """
        if self.first_guess:
            self.first_guess = False
            self.last_guess = [
                ColorCode(1),
                ColorCode(1),
                ColorCode(2),
                ColorCode(2),
                ColorCode(3),
            ]
            return self.last_guess

        if not self.possible_codes:
            return [ColorCode(1) for _ in range(5)]

        # Minimax-Strategie
        best_guess = None
        min_max_remaining = float("inf")

        # Optimierung: Verwende nur eine Stichprobe der möglichen Codes
        sample_size = min(len(self.possible_codes), 100)
        sample_codes = set(list(self.possible_codes)[:sample_size])

        for guess in sample_codes:
            max_remaining = 0

            # Optimierung: Verwende auch hier nur eine Stichprobe
            for possible_code in sample_codes:
                feedback = self._calculate_feedback(list(guess), list(possible_code))
                # Zähle wie viele Codes nach diesem Feedback übrig bleiben würden
                remaining = sum(
                    1
                    for code in self.possible_codes
                    if self._would_give_same_feedback(list(code), feedback)
                )
                max_remaining = max(max_remaining, remaining)

                # Optimierung: Frühzeitiger Abbruch, wenn dieser Guess
                # nicht besser sein kann
                if max_remaining >= min_max_remaining:
                    break

            # Wenn dieser Rateversuch besser ist als der bisherige beste
            if max_remaining < min_max_remaining:
                min_max_remaining = max_remaining
                best_guess = guess
            # Bei gleichem Score bevorzuge einen Code aus possible_codes
            elif max_remaining == min_max_remaining and guess in self.possible_codes:
                best_guess = guess

        self.last_guess = list(best_guess)
        return self.last_guess

    def _calculate_feedback(
        self, guess: List[ColorCode], code: List[ColorCode]
    ) -> List[FeedbackColorCode]:
        """
        Calculate feedback for a guess against the secret code.

        Args:
            guess (List[ColorCode]): The guessed color code.
            code (List[ColorCode]): The secret color code.

        Returns:
            List[FeedbackColorCode]: The feedback for the guess.
        """
        feedback = []
        temp_guess = guess.copy()
        temp_code = code.copy()

        # Prüfe auf exakte Übereinstimmungen (schwarz)
        for i in range(len(temp_code)):
            if temp_guess[i] == temp_code[i]:
                feedback.append(FeedbackColorCode.BLACK)
                temp_code[i] = None
                temp_guess[i] = None

        # Prüfe auf richtige Farben an falscher Position (weiß)
        for i in range(len(temp_guess)):
            if temp_guess[i] is not None and temp_guess[i] in temp_code:
                feedback.append(FeedbackColorCode.WHITE)
                temp_code[temp_code.index(temp_guess[i])] = None

        return feedback

    def process_feedback(self, feedback: List[FeedbackColorCode]) -> None:
        """
        Process feedback and update possible codes.

        Args:
            feedback (List[FeedbackColorCode]): The feedback for the last guess.
        """
        if not self.last_guess:
            return

        self.possible_codes = {
            code
            for code in self.possible_codes
            if self._would_give_same_feedback(list(code), feedback)
        }

    def _would_give_same_feedback(
        self, code: List[ColorCode], target_feedback: List[FeedbackColorCode]
    ) -> bool:
        """
        Check if a code would give the same feedback as the target feedback.

        Args:
            code (List[ColorCode]): The color code to check.
            target_feedback (List[FeedbackColorCode]): The target feedback.

        Returns:
            bool: True if the code would give the same feedback, False otherwise.
        """
        received_feedback = []
        temp_guess = self.last_guess.copy()
        temp_code = code.copy()

        # Prüfe auf exakte Übereinstimmungen (schwarz)
        for i in range(len(temp_code)):
            if temp_guess[i] == temp_code[i]:
                received_feedback.append(FeedbackColorCode.BLACK)
                temp_code[i] = None
                temp_guess[i] = None

        # Prüfe auf richtige Farben an falscher Position (weiß)
        for i in range(len(temp_guess)):
            if temp_guess[i] is not None and temp_guess[i] in temp_code:
                received_feedback.append(FeedbackColorCode.WHITE)
                temp_code[temp_code.index(temp_guess[i])] = None

        # Vergleiche die Anzahl der schwarzen und weißen Pins stattdessen
        black_received = sum(
            1 for f in received_feedback if f == FeedbackColorCode.BLACK
        )
        white_received = sum(
            1 for f in received_feedback if f == FeedbackColorCode.WHITE
        )
        black_target = sum(1 for f in target_feedback if f == FeedbackColorCode.BLACK)
        white_target = sum(1 for f in target_feedback if f == FeedbackColorCode.WHITE)

        return black_received == black_target and white_received == white_target
