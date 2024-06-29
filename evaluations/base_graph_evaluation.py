import time

class BaseGraphEvaluation:
    name = "BaseGraphEvaluation"

    def setup(self):
        # Common setup for all graphs, if any
        pass

    def run_evaluation(self, test_func, *args, **kwargs):
        print(f"Running {test_func.__name__}...")
        start_time = time.time()  # Capture start time
        result = test_func(*args, **kwargs)
        end_time = time.time()  # Capture end time
        duration = end_time - start_time  # Calculate duration
        print("Result:", result)
        print(f"Test completed in {duration:.2f} seconds.\n")