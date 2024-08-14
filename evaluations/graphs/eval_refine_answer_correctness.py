from evaluations.base_graph_evaluation import BaseGraphEvaluation
from src.graphs.graphs import get_refine_answer_correctness_graph, get_generate_question_prompts

class RefineAnswerCorrectnessGraphEvaluation(BaseGraphEvaluation):
    name = "RefineAnswerCorrectnessGraphEvaluation"

    def get_graph(self):
        return get_refine_answer_correctness_graph()
    
    def get_prompts(self):
        return get_generate_question_prompts()

    def eval_completely_correct(self):
        state = {
            'passage': 'Senatores in curia magna colloquuntur de novo decreto. Quisque quid sentiat explicat et argumenta curiam persuadere conatur. Post longam disputationem, consilium commune iniri potest.',
            'generated_question': 'Quid senatores post longam disputationem efficere possunt?',
            'answer': 'Senatores, post longam disputationem inter se, consilium commune iniri possunt.',
        }
        self.run_evaluation(self.graph.invoke, state)

    def eval_completely_incorrect(self):
        state = {
            'passage': 'Senatores in curia magna colloquuntur de novo decreto. Quisque quid sentiat explicat et argumenta curiam persuadere conatur. Post longam disputationem, consilium commune iniri potest.',
            'generated_question': 'Quid senatores post longam disputationem efficere possunt?',
            'answer': 'Senatores, post longam disputationem inter se, consilium commune iniri non possunt.',
        }
        self.run_evaluation(self.graph.invoke, state)