"""Module for computer guesser implementation."""

import time
from itertools import product
from typing import List, Set
from src.GameLogic.Guesser.i_guesser import IGuesser
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


class ComputerGuesser(IGuesser):
    """Computer implementation of the guesser interface.

    This class implements the computer's strategy for guessing the secret code
    using a Knuth-like algorithm.

    Attributes:
        positions: Number of positions in the code
        colors: Number of available colors
        possible_codes: Set of remaining possible codes
        last_guess: Previous guess made by computer
        first_guess: Whether this is the first guess
    """

    def __init__(self: "ComputerGuesser", positions: int, colors: int) -> None:
        """Initialize computer guesser with game parameters.

        Args:
            positions: Number of positions in the code
            colors: Number of available colors
        """
        self.positions = positions
        self.colors = colors
        self.possible_codes = self._generate_all_possible_codes()
        self.last_guess = None
        self.first_guess = True

    def _generate_all_possible_codes(self: "ComputerGuesser") -> Set[tuple]:
        """Generate all possible codes.

        Returns:
            Set[tuple]: A set of all possible color code combinations
        """
        start_time = time.time()
        colors = [ColorCode(i) for i in range(1, self.colors + 1)]
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"generate all poss codes: {elapsed_time:.4f} seconds")
        return set(product(colors, repeat=self.positions))

    def make_guess(self: "ComputerGuesser") -> List[ColorCode]:
        """Make a guess for the secret code.

        Returns:
            List[ColorCode]: The guessed color code

        Raises:
            ValueError: If no valid guesses remain (cheating detected)
        """
        if self.first_guess:
            self.first_guess = False
            if self.colors == 1:
                self.last_guess = [ColorCode(1)] * self.positions
            else:
                self.last_guess = [ColorCode(1)] * (self.positions // 2) + [
                    ColorCode(2)
                ] * (self.positions - self.positions // 2)
            return self.last_guess

        if not self.possible_codes:
            raise ValueError("CHEATING_DETECTED")

        start_time_total = time.time()

        best_guess = None
        min_max_remaining = float("inf")

        for guess in self.possible_codes:
            start_time_guess = time.time()

            max_remaining = 0

            score_counts = {}

            for possible_code in self.possible_codes:
                start_time_feedback = time.time()

                feedback = self._calculate_feedback(list(guess), list(possible_code))
                score = tuple(feedback)
                score_counts[score] = score_counts.get(score, 0) + 1
                max_remaining = max(max_remaining, score_counts[score])
                feedback_time = time.time() - start_time_feedback
                print(f"Feedback calculation time: {feedback_time:.4f} seconds")
                start_time_remaining = time.time()

                remaining_time = time.time() - start_time_remaining
                print(f"Remaining calculation time: {remaining_time:.4f} seconds")

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
        self: "ComputerGuesser", guess: List[ColorCode], code: List[ColorCode]
    ) -> List[FeedbackColorCode]:
        """Calculate feedback for a guess against a code.

        Uses the Mastermind feedback rules:
        - Black pin for correct color in correct position
        - White pin for correct color in wrong position

        Args:
            guess: The guessed color code sequence
            code: The code to compare against

        Returns:
            List of feedback pins (BLACK/WHITE) for the guess
        """

        feedback = []
        temp_guess = guess.copy()
        temp_code = code.copy()

        for i in range(len(temp_code)):
            if temp_guess[i] == temp_code[i]:
                feedback.append(FeedbackColorCode.BLACK)
                temp_code[i] = None
                temp_guess[i] = None

        for i in range(len(temp_guess)):
            if temp_guess[i] is not None and temp_guess[i] in temp_code:
                feedback.append(FeedbackColorCode.WHITE)
                temp_code[temp_code.index(temp_guess[i])] = None

        return feedback

    def process_feedback(
        self: "ComputerGuesser", feedback: List[FeedbackColorCode]
    ) -> None:
        """Process feedback and update possible codes.

        Updates the set of possible codes by eliminating those that would not
        give the same feedback as received.

        Args:
            feedback: The feedback received for the last guess
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
        self: "ComputerGuesser",
        code: List[ColorCode],
        target_feedback: List[FeedbackColorCode],
    ) -> bool:
        """Check if a code would give the same feedback as target.

        Calculates feedback for the code against the last guess and compares
        it with target feedback.

        Args:
            code: Code to check feedback for
            target_feedback: Target feedback to compare against

        Returns:
            True if feedback matches target, False otherwise
        """
        received_feedback = []
        temp_guess = self.last_guess.copy()
        temp_code = code.copy()

        for i in range(len(temp_code)):
            if temp_guess[i] == temp_code[i]:
                received_feedback.append(FeedbackColorCode.BLACK)
                temp_code[i] = None
                temp_guess[i] = None

        for i in range(len(temp_guess)):
            if temp_guess[i] is not None and temp_guess[i] in temp_code:
                received_feedback.append(FeedbackColorCode.WHITE)
                temp_code[temp_code.index(temp_guess[i])] = None

        black_received = sum(
            1 for f in received_feedback if f == FeedbackColorCode.BLACK
        )
        white_received = sum(
            1 for f in received_feedback if f == FeedbackColorCode.WHITE
        )
        black_target = sum(1 for f in target_feedback if f == FeedbackColorCode.BLACK)
        white_target = sum(1 for f in target_feedback if f == FeedbackColorCode.WHITE)

        return black_received == black_target and white_received == white_target
