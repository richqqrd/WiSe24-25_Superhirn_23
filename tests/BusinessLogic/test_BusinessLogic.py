import pytest
from src.BusinessLogic.BusinessLogic import BusinessLogic


@pytest.fixture
def business_logic():
    """
    Fixture to create an instance of BusinessLogic for testing.
    """
    return BusinessLogic()


def test_handle_valid_command(business_logic):
    """
    Test handle method with valid commands.
    """
    assert (
        business_logic.handle("1") == "choose_role"
    ), "Command '1' should start offline game."
    assert (
        business_logic.handle("2") == "choose_role"
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
        business_logic.start_online_game() == "choose_role"
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
