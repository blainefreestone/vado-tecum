import pytest
from unittest.mock import Mock, patch
from src.graphs.generate_question import generate_question, State, question_chain, insight_chain
from langchain_core.messages.ai import AIMessage

@pytest.fixture
def state():
    return State({
        "passage": "This is a test passage.",
        "target_grammar": "test grammar",
    })

def test_question_chain():
    # Test the chain of the generate_question function
    with patch('langchain_openai.ChatOpenAI.invoke', new=Mock()) as mock_invoke:
        mock_invoke.return_value = AIMessage(content="This is a test question.")
        result = question_chain.invoke({
            "passage": "This is a test passage."
        })
        assert result == "This is a test question."

def test_insight_chain():
    # Test the chain of the generate_insight function
    with patch('langchain_openai.ChatOpenAI.invoke', new=Mock()) as mock_invoke:
        mock_invoke.return_value = AIMessage(content="This is a test insight.")
        result = insight_chain.invoke({
            "passage": "This is a test passage."
        })
        assert result == "This is a test insight."

def test_generate_question_node(state):
    # Test the generate_question function
    with patch('langchain_openai.ChatOpenAI.invoke', new=Mock()) as mock_invoke:
        mock_invoke.return_value = AIMessage(content="This is a test question.")
        result = generate_question(state)
        assert result["generated_question"] == "This is a test question."

def test_generate_insight_node(state):
    # Test the generate_insight function
    with patch('langchain_openai.ChatOpenAI.invoke', new=Mock()) as mock_invoke:
        mock_invoke.return_value = AIMessage(content="This is a test insight.")
        result = generate_question(state)
        assert result["generated_insight"] == "This is a test insight."