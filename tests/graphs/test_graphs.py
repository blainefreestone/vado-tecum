import pytest
from src.graphs import graphs
from langgraph.graph.state import CompiledGraph

def test_get_generate_question_graph():
    result = graphs.get_generate_question_graph()
    assert isinstance(result, CompiledGraph)

def test_get_generate_question_prompts():
    result = graphs.get_generate_question_prompts()
    assert isinstance(result, dict)