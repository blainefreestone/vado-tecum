import argparse
from evaluations.base_graph_evaluation import BaseGraphEvaluation
from evaluations.graphs.eval_generate_question import GenerateQuestionGraphEvaluation

evaluation_classes = [
    GenerateQuestionGraphEvaluation
]

def run_all_evaluations():
    for evaluation_class in evaluation_classes:
        print(f"Running evaluations for {evaluation_class.name}...")
        evaluation_instance = evaluation_class()
        evaluation_instance.setup()
        # Run all evaluations defined in the evaluation class
        for method in dir(evaluation_instance):
            if method.startswith("eval_"):
                evaluation_method = getattr(evaluation_instance, method)
                evaluation_instance.run_evaluation(evaluation_method)

def run_specific_evaluation(graph_name):
    # Map graph names to evaluation classes
    graph_evaluations = {}
    for evaluation_class in evaluation_classes:
        graph_evaluations[evaluation_class.name] = evaluation_class

    if graph_name in graph_evaluations:
        evaluation_class = graph_evaluations[graph_name]()
        print(f"Running evaluations for {graph_name}...")
        evaluation_class.setup()
        for method in dir(evaluation_class):
            if method.startswith("eval_"):
                evaluation_method = getattr(evaluation_class, method)
                evaluation_class.run_evaluation(evaluation_method)
    else:
        print(f"No evaluations found for graph: {graph_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run graph evaluations.")
    parser.add_argument("-a", "--all", help="Run all evaluations", action="store_true")
    parser.add_argument("-g", "--graph", help="Run evaluations for a specific graph", type=str)

    args = parser.parse_args()

    if args.all:
        run_all_evaluations()
    elif args.graph:
        run_specific_evaluation(args.graph)
    else:
        print("No arguments provided. Use -a to run all evaluations or -g <GRAPH_NAME> to run specific evaluations.")