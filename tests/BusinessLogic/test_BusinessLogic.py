from unittest.mock import Mock

import pytest
from src.BusinessLogic.BusinessLogic import BusinessLogic
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode


@pytest.fixture
def game_logic():
    return Mock()

@pytest.fixture
def business_logic(game_logic):
    """
    Fixture to create an instance of BusinessLogic for testing.
    """
    return BusinessLogic(game_logic)


def test_handle_valid_command(business_logic):
    """
    Test handle method with valid commands.
    """
    assert (
        business_logic.handle("1") == "choose_role"
    ), "Command '1' should start offline game."
    assert (
        business_logic.handle("2") == "choose_role_online"
    ), "Command '2' should start online game."
    assert (
        business_logic.handle("3") == "choose_language"
    ), "Command '3' should change language."
    assert business_logic.handle("4") == "end_game", "Command '4' should end game."
    assert business_logic.handle("5") == "save_game", "Command '5' should save game."
    assert (
        business_logic.handle("6") == "resume_interrupted_game"
    ), "Command '6' should resume game."


def test_handle_invalid_command(business_logic):
    """
    Test handle method with an invalid command.
    """
    assert (
        business_logic.handle("invalid") == "Invalid command."
    ), "Invalid commands should return 'Invalid command'."
    assert business_logic.handle("0") == "Invalid command.", "Command '0' is not valid."
    assert (
        business_logic.handle("7") == "Invalid command."
    ), "Command '7' is not mapped."


def test_start_offline_game(business_logic):
    """
    Test start_offline_game method.
    """
    assert (
        business_logic.start_offline_game() == "choose_role"
    ), "Offline game should prompt to choose role."


def test_start_online_game(business_logic):
    """
    Test start_online_game method.
    """
    assert (
        business_logic.start_online_game() == "choose_role_online"
    ), "Online game should prompt to choose role."


def test_change_language(business_logic):
    """
    Test change_language method.
    """
    assert (
        business_logic.change_language() == "choose_language"
    ), "Language change should prompt to choose language."


def test_end_game(business_logic):
    """
    Test end_game method.
    """
    assert (
        business_logic.end_game() == "end_game"
    ), "Ending game should return 'end_game'."


def test_save_game(business_logic):
    """
    Test save_game method.
    """
    assert (
        business_logic.save_game() == "save_game"
    ), "Saving game should return 'save_game'."


def test_resume_interrupted_game(business_logic):
    """
    Test resume_interrupted_game method.
    """
    assert (
        business_logic.resume_interrupted_game() == "resume_interrupted_game"
    ), "Resuming interrupted game should return 'resume_interrupted_game'."

def test_convert_to_color_code(business_logic):
    """
    Test _convert_to_color_code method.
    """
    for i in range(1, 9):
        color = business_logic._convert_to_color_code(i)
        match i:
            case 1: assert color == ColorCode.RED
            case 2: assert color == ColorCode.GREEN
            case 3: assert color == ColorCode.YELLOW
            case 4: assert color == ColorCode.BLUE
            case 5: assert color == ColorCode.ORANGE
            case 6: assert color == ColorCode.BROWN
            case 7: assert color == ColorCode.WHITE
            case 8: assert color == ColorCode.BLACK

    with pytest.raises(ValueError):
        business_logic._convert_to_color_code(9)

def test_is_valid_code(business_logic):
    """
    Test _is_valid_code method.
    """
    assert not business_logic._is_valid_code("1")
    assert not business_logic._is_valid_code("12349")
    assert business_logic._is_valid_code("12345")

def test_is_valid_feedback(business_logic):
    """
    Test _is_valid_feedback method.
    """
    assert not business_logic._is_valid_feedback("1")
    assert not business_logic._is_valid_feedback("777777")
    assert business_logic._is_valid_feedback("")
    assert business_logic._is_valid_feedback("78787")
    assert business_logic._is_valid_feedback("88888")

def test_handle_feedback_input(business_logic, game_logic):
    """
    Test handle_feedback_input method.
    """
    assert business_logic.handle_feedback_input("1") == "need_feedback_input"

    game_logic.set_feedback.return_value = "game_over"
    assert business_logic.handle_feedback_input("88888") == "game_over"
    game_logic.set_feedback.assert_called_once_with([
        FeedbackColorCode.BLACK, FeedbackColorCode.BLACK,
        FeedbackColorCode.BLACK, FeedbackColorCode.BLACK,
        FeedbackColorCode.BLACK
    ])

def test_handle_code_input(business_logic, game_logic):
    """
    Test handle_feedback_input method.
    """
    assert business_logic.handle_code_input("1") == "need_code_input"

    game_logic.set_secret_code.return_value = "wait_for_computer_guess"
    assert business_logic.handle_code_input("12345") == "wait_for_computer_guess"
    game_logic.set_secret_code.assert_called_once_with([
        ColorCode.RED, ColorCode.GREEN, ColorCode.YELLOW,
        ColorCode.BLUE, ColorCode.ORANGE
    ])

def test_handle_guess_input(business_logic, game_logic):
    """
    Test handle_feedback_input method.
    """
    assert business_logic.handle_guess_input("1") == "need_guess_input"

    game_logic.make_guess.return_value = "game_over"
    assert business_logic.handle_guess_input("12345") == "game_over"
    game_logic.make_guess.assert_called_once_with([
        ColorCode.RED, ColorCode.GREEN, ColorCode.YELLOW,
        ColorCode.BLUE, ColorCode.ORANGE
    ])

def test_handle_role_choice(business_logic, game_logic):
    """
    Test handle_feedback_input method.
    """
    assert business_logic.handle_role_choice("0", "online") == "Invalid role."

    game_logic.startgame.return_value = "need_guess_input"
    assert business_logic.handle_role_choice("1", "offline") == "need_guess_input"
    game_logic.startgame.assert_called_once_with("guesser")
