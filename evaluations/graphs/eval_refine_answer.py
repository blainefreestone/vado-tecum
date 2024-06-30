from evaluations.base_graph_evaluation import BaseGraphEvaluation
from app.graphs.graphs import get_refine_answer_graph, get_refine_answer_prompts

class RefineAnswerGraphEvaluation(BaseGraphEvaluation):
    name = "RefineAnswerGraphEvaluation"

    def get_graph(self):
        return get_refine_answer_graph()
    
    def get_prompts(self):
        return get_refine_answer_prompts()
    
    def eval_excellent_answer(self):
        state = {
            'passage': 'Senatores in curia magna colloquuntur de novo decreto. Quisque quid sentiat explicat et argumenta curiam persuadere conatur. Post longam disputationem, consilium commune iniri potest.',
            'target_grammar': 'reciprocal pronouns',
            'generated_question': 'Quid senatores post longam disputationem efficere possunt?',
            'answer': 'Senatores, post longam disputationem inter se, consilium commune iniri possunt.',
        }
        self.run_evaluation(self.graph.invoke, state)

    def eval_irrelevant_answer(self):
        state = {
            'passage': 'Senatores in curia magna colloquuntur de novo decreto. Quisque quid sentiat explicat et argumenta curiam persuadere conatur. Post longam disputationem, consilium commune iniri potest.',
            'target_grammar': 'reciprocal pronouns',
            'generated_question': 'Quid senatores post longam disputationem efficere possunt?',
            'answer': 'Senatores inter se collocuti sunt de novo decreto.',
        }
        self.run_evaluation(self.graph.invoke, state)

    def eval_incorrect_answer(self):
        state = {
            'passage': 'Senatores in curia magna colloquuntur de novo decreto. Quisque quid sentiat explicat et argumenta curiam persuadere conatur. Post longam disputationem, consilium commune iniri potest.',
            'target_grammar': 'reciprocal pronouns',
            'generated_question': 'Quid senatores post longam disputationem efficere possunt?',
            'answer': 'Senatores, post longam disputationem inter se, consilium commune iniri non possunt.',
        }
        self.run_evaluation(self.graph.invoke, state)

    def eval_excluding_grammar_target_answer(self):
        state = {
            'passage': 'Senatores in curia magna colloquuntur de novo decreto. Quisque quid sentiat explicat et argumenta curiam persuadere conatur. Post longam disputationem, consilium commune iniri potest.',
            'target_grammar': 'reciprocal pronouns',
            'generated_question': 'Quid senatores post longam disputationem efficere possunt?',
            'answer': 'Senatores, post longam disputationem, consilium commune iniri possunt.',
        }
        self.run_evaluation(self.graph.invoke, state)