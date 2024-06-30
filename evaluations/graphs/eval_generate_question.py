from evaluations.base_graph_evaluation import BaseGraphEvaluation
from app.graphs.graphs import get_generate_question_graph, get_generate_question_prompts

class GenerateQuestionGraphEvaluation(BaseGraphEvaluation):
    name = "GenerateQuestionGraphEvaluation"

    def get_graph(self):
        return get_generate_question_graph()
    
    def get_prompts(self):
        return get_generate_question_prompts()

    def eval_reciprocal_pronouns(self):
        state = {
            'passage': 'Senatores in curia magna colloquuntur de novo decreto. Quisque quid sentiat explicat et argumenta curiam persuadere conatur. Post longam disputationem, consilium commune iniri potest.',
            'target_grammar': 'reciprocal pronouns'
        }
        self.run_evaluation(self.graph.invoke, state)

    def eval_genetive_of_ownership(self):
        state = {
            'passage': 'Tantae molis erat Romanam condere gentem, quae terris, quae maribus, quae aere vasto, ' \
                        'tridentibus aequor, patres, abdiderat populumque, iura legesque dabat.',
            'target_grammar': 'genitive of ownership'
        }
        self.run_evaluation(self.graph.invoke, state)

    def eval_indirect_questions(self):
        state = {
            'passage': 'Senator ad forum venit et magnā voce locutus est. Cīvēs de statu rērum sollicitī erant. ' \
                        'Post longum colloquium, populus laetus discessit.',
            'target_grammar': 'indirect questions'
        }
        self.run_evaluation(self.graph.invoke, state)

    def eval_gerund(self):
        state = {
            'passage': 'Senex in horto suo arbores curat et flores plantat. Multa tempora in horto consumit, '\
                        'interdum cum amicis colloquitur. Senex gaudet cum flores videt crescere et arbores ' \
                        'fruges ferre. Hic hortus est ei locus quietis et meditationis.',
            'target_grammar': 'gerund'
        }
        self.run_evaluation(self.graph.invoke, state)