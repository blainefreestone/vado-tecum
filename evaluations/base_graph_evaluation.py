import time
import pprint

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
        result = test_func(*args, **kwargs)
        end_time = time.time()  # Capture end time
        duration = end_time - start_time  # Calculate duration
        print("Result: ", end="")
        pprint.pprint(result, indent=4)
        print(f"Test completed in {duration:.2f} seconds.\n")