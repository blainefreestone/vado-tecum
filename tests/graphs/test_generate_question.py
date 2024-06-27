import pytest
from unittest.mock import Mock, patch
from app.graphs.generate_question import generate_question, State, chain
from langchain_core.messages.ai import AIMessage

@pytest.fixture
def state():
    return State({
        "passage": "This is a test passage.",
    })

def test_chain():
    # Test the chain of the generate_question function
    with patch('langchain_openai.ChatOpenAI.invoke', new=Mock()) as mock_invoke:
        mock_invoke.return_value = AIMessage(content="This is a test question.")
        result = chain.invoke({
            "passage": "This is a test passage."
        })
        assert result == "This is a test question."

def test_generate_question(state):
    # Test the generate_question function
    with patch('langchain_openai.ChatOpenAI.invoke', new=Mock()) as mock_invoke:
        mock_invoke.return_value = AIMessage(content="This is a test question.")
        result = generate_question(state)
        assert result["generated_question"] == "This is a test question."