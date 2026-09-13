import json
import os
import argparse
if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Evaluation script for colours_present task")
    parser.add_argument(
        '--answer', '-a',
        type=str,
        default='answer.json',
        help='Path to the answer JSON file (default: answer.json)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='eval.json',
        help='Path to the output JSON file (default: eval.json)'
    )
    parser.add_argument(
        '--gold', '-g',
        type=str,
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json'),
        help='Path to the reference data.json (default: data.json next to this script)'
    )
    args = parser.parse_args()
    with open(args.answer, 'r') as f:
        data = json.load(f)

    # Gold labels always come from the reference data.json (matched on 'id'), never from the
    # answer file. Until 2026-09-11, data.json listed the yes/no answers in a different colour
    # order than prompts/rules.txt, and answer files built from it still carry those labels.
    with open(args.gold, 'r') as f:
        reference = {entry['id']: entry for entry in json.load(f)}

    # Initialize variables to calculate accuracies
    correct_counts = 0
    total_counts = 0
    outdated_gold = 0
    category_accuracies = {}

    # Iterate through the JSON data
    for entry in data:
        if entry['id'] not in reference:
            raise KeyError(f"id {entry['id']!r} from {args.answer} is not in {args.gold}")
        gold = reference[entry['id']]
        num_objects = gold['num_objects']
        colours_present = [s.lower() for s in gold['colours_present']]
        if 'colours_present' in entry and [str(s).lower() for s in entry['colours_present']] != colours_present:
            outdated_gold += 1

        total_counts += 1

        # Calculate per-category accuracy
        if num_objects not in category_accuracies:
            category_accuracies[num_objects] = {'correct': 0, 'total': 0}

        category_accuracies[num_objects]['total'] += 1

        try:
            prediction = entry['Output']
            prediction = [s.lower() for s in prediction]
        except:
            continue
        # Check if the prediction is correct
        if colours_present == prediction:
            correct_counts += 1
            category_accuracies[num_objects]['correct'] += 1

    # Calculate overall accuracy
    overall_accuracy = correct_counts / total_counts * 100

    # Calculate accuracy for each category
    category_accuracy_percentages = {
        k: (v['correct'] / v['total'] * 100) for k, v in category_accuracies.items()
    }

    # Prepare results for saving
    eval_results = {
        "Overall Accuracy": overall_accuracy,
        "Category-wise Accuracy": category_accuracy_percentages
    }

    # Save results to eval.json
    with open(args.output, 'w') as eval_file:
        json.dump(eval_results, eval_file, indent=4)

    if outdated_gold:
        print(f"Note: {outdated_gold} of {total_counts} answer records carry outdated 'colours_present' labels; "
              f"they were scored against {args.gold} instead.")
    print("Evaluation results saved to " + args.output)

