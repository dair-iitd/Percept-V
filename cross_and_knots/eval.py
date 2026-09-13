import json
import argparse

def eval(data):
    # Initialize variables to calculate accuracies
    correct_counts = 0
    total_counts = 0
    category_accuracies = {}

    # Iterate through the JSON data

    for entry in data:
        grid_size = entry['n']
        num_circles = entry['crosses']
        total_counts += 1

        # Calculate per-category accuracy
        #if grid_size not in category_accuracies:
        #    category_accuracies[grid_size] = {'correct': 0  , 'total': 0}
        
        if num_circles not in category_accuracies:
            category_accuracies[num_circles] = {'correct': 0, 'total': 0}

        category_accuracies[num_circles]['total'] += 1
        #category_accuracies['total'] += 1
        # category_accuracies[(grid_size,num_circles)]['total'] += 1

        if entry["ERROR"]:
            continue

        # Check if the output is correct
        output = entry["Output"]

        if output is None:
            if len(entry["gold_output"]) == 0:
                correct_counts += 1
                category_accuracies[num_circles]['correct'] += 1
        else:
            if output in entry["gold_output"]:
                correct_counts += 1
                category_accuracies[num_circles]['correct'] += 1

    # Calculate overall accuracy
    overall_accuracy = correct_counts / total_counts * 100

    category_accuracy_percentages = {
        k: (v['correct'] / v['total'] * 100) for k, v in category_accuracies.items()
    }

    #Calculate standard deviation
    category_stdevs = {
        k: (((1-category_accuracy_percentages[k]/100)**2)*(category_accuracy_percentages[k]/100))**0.5 for k, _ in category_accuracies.items()
    }

    # Prepare results for saving
    eval_results = {
        "Overall Accuracy": overall_accuracy,
        "Category-wise Accuracy": category_accuracy_percentages,
        "Category-wise Stdev": category_stdevs
    }

    return eval_results

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Evaluation script for comparing_size task")
    parser.add_argument(
        '--answer', '-a',
        type=str,
        default='answer_gpt4o.json',
        help='Path to the answer JSON file (default: answer.json)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='eval_gpt4o.json',
        help='Path to the output JSON file (default: eval.json)'
    )
    args = parser.parse_args()
    data = {}
    # Assuming your JSON data is stored in a file called 'results.json'
    with open(args.answer, 'r') as f:
        data = json.load(f)

    eval_results = eval(data)

    # Save results to eval.json
    with open(args.output, 'w') as eval_file:
        json.dump(eval_results, eval_file, indent=4)

    print("Evaluation results saved to eval.json.")