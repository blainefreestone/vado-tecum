from evaluations.base_graph_evaluation import BaseGraphEvaluation
from src.graphs.graphs import get_refine_answer_relevance_graph, get_refine_answer_relevance_prompts

class RefineAnswerRelevanceGraphEvaluation(BaseGraphEvaluation):
    name = "RefineAnswerRelevanceGraphEvaluation"

    def get_graph(self):
        return get_refine_answer_relevance_graph()
    
    def get_prompts(self):
        return get_refine_answer_relevance_prompts()

    def eval_completely_irrelevant(self):
        state = {
            'passage': 'Senex in horto suo arbores curat et flores plantat. Multa tempora in horto consumit, interdum cum amicis colloquitur. Senex gaudet cum flores videt crescere et arbores fruges ferre. Hic hortus est ei locus quietis et meditationis.',
            'generated_question': 'Cur senex multa tempora in horto consumit?',
            'answer': 'Senex est qui multos annos vitae habet.',
        }
        self.run_evaluation(self.graph.invoke, state)

    def eval_completely_relevant(self):
        state = {
            'passage': 'Senex in horto suo arbores curat et flores plantat. Multa tempora in horto consumit, interdum cum amicis colloquitur. Senex gaudet cum flores videt crescere et arbores fruges ferre. Hic hortus est ei locus quietis et meditationis.',
            'generated_question': 'Cur senex multa tempora in horto consumit?',
            'answer': 'Curando arbores florisque plantando, senex multa tempora in horto consumit.',
        }
        self.run_evaluation(self.graph.invoke, state)