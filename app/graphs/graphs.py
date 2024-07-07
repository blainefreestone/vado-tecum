# graphs.py

from . import generate_question
from . import refine_answer
from . import refine_answer_relevance
from . import refine_answer_correctness

def get_generate_question_graph():
    return generate_question.get_graph()

def get_generate_question_prompts():
    return generate_question.get_prompts()

def get_refine_answer_graph():
    return refine_answer.get_graph()

def get_refine_answer_prompts():
    return refine_answer.get_prompts()

def get_refine_answer_relevance_graph():
    return refine_answer_relevance.get_graph()

def get_refine_answer_relevance_prompts():
    return refine_answer_relevance.get_prompts()

def get_refine_answer_correctness_graph():
    return refine_answer_correctness.get_graph()

def get_refine_answer_correctness_prompts():
    return refine_answer_correctness.get_prompts()