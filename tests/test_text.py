import pytest
from app.text import Text

@pytest.fixture
def text():
    return Text("Test Title", "Blaine Freestone", [["Chapter 1", "Text2"], ["Chapter 2", "Text2"], ["Chapter 3", "Text3"]])

def test_text_initialization(text):
    # Test that a Text object is correctly initialized
    assert text.content == [["Chapter 1", "Text2"], ["Chapter 2", "Text2"], ["Chapter 3", "Text3"]]
    assert text.title == "Test Title"
    assert text.author == "Blaine Freestone"

def test_get_text(text):
    # Test the get_paragraph method
    assert text.get_paragraph((1, 1)) == "Chapter 1"
    assert text.get_paragraph((1, 2)) == "Text2"
    assert text.get_paragraph((4, 4)) == None

    # Test the get_chapter method
    assert text.get_chapter(1) == "Chapter 1\nText2"
    assert text.get_chapter(2) == "Chapter 2\nText2"
    assert text.get_chapter(4) == None

    # Test the __str__ method
    assert str(text) == "Test Title\nBlaine Freestone\n\nChapter 1\nText2\n\nChapter 2\nText2\n\nChapter 3\nText3"

def test_from_string(text):
    # Test the from_string method
    text = Text.from_string("Test Title\nBlaine Freestone\n\nChapter 1\nText2\n\nChapter 2\nText2\n\nChapter 3\nText3")
    assert text.title == "Test Title"
    assert text.author == "Blaine Freestone"
    assert text.content == [["Chapter 1", "Text2"], ["Chapter 2", "Text2"], ["Chapter 3", "Text3"]]

def test_from_file(tmp_path, text):
    # Test the from_file method
    file = tmp_path / "test_file.txt"
    file.write_text("Test Title\nBlaine Freestone\n\nChapter 1\nText2\n\nChapter 2\nText2\n\nChapter 3\nText3")
    text = Text.from_file(file)
    assert text.title == "Test Title"
    assert text.author == "Blaine Freestone"
    assert text.content == [["Chapter 1", "Text2"], ["Chapter 2", "Text2"], ["Chapter 3", "Text3"]]