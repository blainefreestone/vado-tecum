from evaluations.base_graph_evaluation import BaseGraphEvaluation
from app.graphs.graphs import get_generate_question_graph

class GenerateQuestionGraphEvaluation(BaseGraphEvaluation):
    name = "GenerateQuestionGraphEvaluation"

    def __init__(self):
        self.graph = get_generate_question_graph()   

    def eval_simple_passage(self):
        state = {'passage': 'Tantae molis erat Romanam condere gentem.'}
        self.run_evaluation(self.graph.invoke, state)

    def eval_complex_passage(self):
        state = {'passage': 'Tantae molis erat Romanam condere gentem, quae terris, quae maribus, quae aere vasto, ' +
                            'tridentibus aequor, patres, abdiderat populumque, iura legesque dabat.'}
        self.run_evaluation(self.graph.invoke, state)