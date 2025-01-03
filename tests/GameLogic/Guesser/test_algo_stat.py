import time
import unittest
from itertools import product

from src.business_logic.guesser.computer_guesser import ComputerGuesser
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


class TestAlgorithmStatistics(unittest.TestCase):
    def test_algorithm_statistics(self):
        """Test the performance of the computer guesser algorithm."""
        guesser = ComputerGuesser()
        stats = {
            "total_games": 0,
            "successful_games": 0,
            "total_guesses": 0,
            "avg_time_per_guess": 0,
            "max_guesses": 0,
            "games_data": [],
        }

        all_codes = list(product([ColorCode(i) for i in range(1, 9)], repeat=5))
        total_time_start = time.time()

        print(f"\nTesting {len(all_codes)} possible combinations...")

        for test_code in all_codes:
            game_start_time = time.time()
            game_data = {
                "secret_code": test_code,
                "guesses": [],
                "times": [],
                "found": False,
            }

            guesser = ComputerGuesser()

            for attempt in range(10):
                guess_start = time.time()
                guess = guesser.make_guess()
                guess_time = time.time() - guess_start

                game_data["guesses"].append(guess)
                game_data["times"].append(guess_time)

                feedback = guesser._calculate_feedback(guess, list(test_code))

                if all(f == FeedbackColorCode.BLACK for f in feedback):
                    game_data["found"] = True
                    stats["successful_games"] += 1
                    break

                guesser.process_feedback(feedback)

            game_time = time.time() - game_start_time
            stats["total_games"] += 1
            stats["total_guesses"] += len(game_data["guesses"])
            stats["max_guesses"] = max(stats["max_guesses"], len(game_data["guesses"]))
            stats["games_data"].append(game_data)

            # Detaillierte Ausgabe für jeden Code
            print(
                f"\nCode {stats['total_games']}/{len(all_codes)}: {[c.value for c in test_code]}"
            )
            print(f"Found: {game_data['found']}")
            print(f"Attempts: {len(game_data['guesses'])}")
            print(f"Time: {game_time:.2f}s")
            print(
                f"Average time per guess: {sum(game_data['times']) / len(game_data['times']):.2f}s"
            )
