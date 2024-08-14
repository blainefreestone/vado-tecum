import pytest
from src.user_text import UserText
from src.user import User
from src.text import Text

@pytest.fixture
def user():
    return User("Test User")

@pytest.fixture
def text():
    return Text.from_string("Test Title\nBlaine Freestone\n\nChapter 1\nText2\n\nChapter 2\nText2\n\nChapter 3\nText3")

@pytest.fixture
def user_text(text, user):
    return UserText(text, user)

def test_user_text_initialization(user_text, text, user):
    # Test that a UserText object is correctly initialized
    assert user_text.text == text
    assert user_text.user == user
    assert user_text.location == (1, 1)

def test_user_text_update_location(user_text):
    # Test that the location of a UserText object is correctly updated
    user_text.update_location(2, 2)
    assert user_text.location == (2, 2)

    user_text.update_location(3, 2)
    assert user_text.location == (3, 2)

    user_text.update_location(5, 1)
    assert user_text.location == (3, 2)