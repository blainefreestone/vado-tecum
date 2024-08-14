import pytest
from src.user import User
from src.text import Text
from src.user_text import UserText

@pytest.fixture
def user():
    return User("Test User")

@pytest.fixture
def text_first():
    return Text.from_string("Test Title\nBlaine Freestone\n\nChapter 1\nText2\n\nChapter 2\nText2\n\nChapter 3\nText3")

@pytest.fixture
def text_second():
    return Text.from_string("Modified Test Title 2\nModified Blaine Freestone\n\nModified Chapter 1\nModified Text2\n\nModified Chapter 2\nModified Text2\n\nModified Chapter 3\nModified Text3")

def test_user_initialization(user):
    # Test that a User is correctly initialized
    assert user.name == "Test User"

def test_user_str(user):
    assert str(user) == "User: Test User"

def test_assign_text(user, text_first, text_second):
    # Test the assign_text method
    user.assign_text(text_first)
    user.assign_text(text_second)
    assert user.texts[0].text == text_first and user.texts[0].user == user
    assert user.texts[1].text == text_second and user.texts[1].user == user