class BaseGraphEvaluation:
    name = "BaseGraphEvaluation"

    def setup(self):
        # Common setup for all graphs, if any
        pass

    def run_evaluation(self, test_func, *args, **kwargs):
        # Generic test execution logic
        print(f"Running {test_func.__name__}...")
        result = test_func(*args, **kwargs)
        print("Result:", result)
        print("Test completed.\n")