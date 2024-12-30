import time
from collections import Counter
from itertools import product
import random
from typing import List, Set
from src.GameLogic.Guesser.IGuesser import IGuesser
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode


class ComputerGuesser(IGuesser):
    def __init__(self, positions: int, colors: int):
        self.positions = positions
        self.colors = colors
        self.possible_codes = self._generate_all_possible_codes()
        self.last_guess = None
        self.first_guess = True

    def _generate_all_possible_codes(self) -> Set[tuple]:
        """
        Generate all possible codes.

        Returns:
            Set[tuple]: A set of all possible color code combinations.
        """
        start_time = time.time()
        colors = [ColorCode(i) for i in range(1, self.colors+1)]
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"generate all poss codes: {elapsed_time:.4f} seconds")
        return set(product(colors, repeat=self.positions))

    def make_guess(self) -> List[ColorCode]:
        """
        Make a guess for the secret code.

        Returns:
            List[ColorCode]: The guessed color code.
        """
        if self.first_guess:
            self.first_guess = False
            self.last_guess = ([ColorCode(1)] * (self.positions // 2) + 
                             [ColorCode(2)] * (self.positions - self.positions // 2))
            return self.last_guess

        if not self.possible_codes:
            raise ValueError("CHEATING_DETECTED")

        start_time_total = time.time()  # Gesamtdauer des Guess

        # Minimax-Strategie
        best_guess = None
        min_max_remaining = float('inf')

        for guess in self.possible_codes: #new
            start_time_guess = time.time()  # Zeit für diese Vermutung

            max_remaining = 0

            score_counts = {}  #new

            # Optimierung: Verwende auch hier nur eine Stichprobe
            for possible_code in self.possible_codes: #new
                start_time_feedback = time.time()  # Zeit für Feedback-Berechnung

                feedback = self._calculate_feedback(list(guess), list(possible_code))
                score = tuple(feedback)  #new
                score_counts[score] = score_counts.get(score, 0) + 1  #new
                max_score = max(max_remaining, score_counts[score])  #new
                feedback_time = time.time() - start_time_feedback
                print(f"Feedback calculation time: {feedback_time:.4f} seconds")
                # Zähle wie viele Codes nach diesem Feedback übrig bleiben würden
                start_time_remaining = time.time()


                remaining_time = time.time() - start_time_remaining
                print(f"Remaining calculation time: {remaining_time:.4f} seconds")
                #old max_remaining = max(max_remaining, remaining)

            guess_time = time.time() - start_time_guess
            print(f"Time for this guess evaluation: {guess_time:.4f} seconds")

            if max_remaining < min_max_remaining:
                min_max_remaining = max_remaining
                best_guess = guess
                if guess in self.possible_codes:
                    break

        total_time = time.time() - start_time_total
        print(f"Total time for this guess: {total_time:.4f} seconds")
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

        start_time = time.time()

        self.possible_codes = {
            code
            for code in self.possible_codes
            if self._would_give_same_feedback(list(code), feedback)
        }
        process_time = time.time() - start_time
        print(f"Feedback processing time: {process_time:.4f} seconds")

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
