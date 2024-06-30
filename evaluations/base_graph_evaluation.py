import time
import pprint
from langchain_community.callbacks import get_openai_callback

class BaseGraphEvaluation:
    name = "BaseGraphEvaluation"

    def setup(self):
        self.graph = self.get_graph()
        self.graph.get_graph().print_ascii()
        print("\n")
        pprint.pprint(self.get_prompts(), indent=4)
        print("\n")

    def get_graph(self):
        raise NotImplementedError("Subclasses must implement get_graph method.")
    
    def get_prompts(self):
        raise NotImplementedError("Subclasses must implement get_prompts method.")

    def run_evaluation(self, test_func, *args, **kwargs):
        print(f"Running {test_func.__name__}...")
        start_time = time.time()  # Capture start time
        with get_openai_callback() as cb:
            result = test_func(*args, **kwargs)
            total_tokens = cb.total_tokens
            total_cost = cb.total_cost
        end_time = time.time()  # Capture end time
        duration = end_time - start_time  # Calculate duration
        print("Result: ", end="")
        pprint.pprint(result, indent=4)
        print(f"Test completed in {duration:.2f} seconds.")
        print(f"Total tokens: {total_tokens}")
        print(f"Total cost: {total_cost}\n")