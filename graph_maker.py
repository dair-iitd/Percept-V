import json
import matplotlib.pyplot as plt
import sys
import os
import numpy as np
import argparse

# Function to read data from a JSON file
def read_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to plot the data
# def plot_accuracy(data , domain_name , x_label = 'Grid Dimensions'):
#     overall_accuracy = data["Overall Accuracy"]
#     category_accuracy = data["Category-wise Accuracy"]

#     # Extract category names and accuracies
#     categories = list(map(int, category_accuracy.keys()))  # Convert category keys to integers for proper plotting
#     accuracies = list(category_accuracy.values())

#     # Sort categories and accuracies for proper plotting
#     sorted_categories, sorted_accuracies = zip(*sorted(zip(categories, accuracies)))

#     # Plot Category-wise Accuracy
#     plt.figure(figsize=(10, 6))
#     plt.plot(sorted_categories, sorted_accuracies, marker='o', color='blue', label="Category-wise Accuracy")

#     # Add the Overall Accuracy as a horizontal line
#     plt.axhline(y=overall_accuracy, color='red', linestyle='--', label=f"Overall Accuracy: {overall_accuracy:.2f}%")

#     # Add labels and title
#     plt.xlabel(x_label)
#     plt.ylabel('Accuracy (%)')
#     plt.title('Category-wise Accuracy vs Overall Accuracy')
#     plt.xticks(sorted_categories)  # Ensure all categories are shown on x-axis
#     plt.legend()

#     # Show the plot
#     # plt.show()

#     save_path = os.path.join(domain_name, 'accuracy_graph.png')
#     plt.savefig(save_path)
#     plt.close()

# Function to plot the data
def plot_accuracy(data, domain_name, output, x_label='Grid Dimensions', bucket_size=1):
    
    if bucket_size > 1:
        overall_accuracy = data["Overall Accuracy"]
        category_accuracy = data["Category-wise Accuracy"]

        # Extract category names and accuracies
        categories = list(map(int, category_accuracy.keys()))  # Convert category keys to integers for proper plotting
        accuracies = list(category_accuracy.values())
        
        # Sort categories and accuracies for proper plotting
        sorted_categories, sorted_accuracies = zip(*sorted(zip(categories, accuracies)))

        bucket_labels = []
        bucket_accuracies = []
        
        min_cat, max_cat = min(sorted_categories), max(sorted_categories)
        buckets = [(i, i + bucket_size - 1) for i in range(min_cat, max_cat + 1, bucket_size)]
        
        for bucket in buckets:
            bucket_range = range(bucket[0], bucket[1] + 1)
            bucket_values = [acc for cat, acc in zip(sorted_categories, sorted_accuracies) if cat in bucket_range]
            
            if bucket_values:
                bucket_labels.append(f'{bucket[0]}-{bucket[1]}')
                bucket_accuracies.append(np.mean(bucket_values))  # Compute mean accuracy for the bucket
        
        sorted_categories, sorted_accuracies = bucket_labels, bucket_accuracies
    
        # Plot Category-wise Accuracy
        plt.figure(figsize=(10, 6))
        plt.plot(sorted_categories, sorted_accuracies, marker='o', color='blue', label="Category-wise Accuracy")
        
        # Add the Overall Accuracy as a horizontal line
        plt.axhline(y=overall_accuracy, color='red', linestyle='--', label=f"Overall Accuracy: {overall_accuracy:.2f}%")
        
        # Add labels and title
        plt.ylim(0, 100)
        plt.xlabel(x_label)
        plt.ylabel('Accuracy (%)')
        plt.title('Category-wise Accuracy vs Overall Accuracy')
        plt.xticks(rotation=45)  # Rotate for better readability if using bucket labels
        plt.legend()
        
        # Save the plot
        save_path = os.path.join(domain_name, f'accuracy_graph_{bucket_size}.png')
        plt.savefig(save_path)
        plt.close()
    else:
        overall_accuracy = data["Overall Accuracy"]
        category_accuracy = data["Category-wise Accuracy"]

        # Extract category names and accuracies
        categories = list(map(int, category_accuracy.keys()))  # Convert category keys to integers for proper plotting
        accuracies = list(category_accuracy.values())

        # Sort categories and accuracies for proper plotting
        sorted_categories, sorted_accuracies = zip(*sorted(zip(categories, accuracies)))

        # Plot Category-wise Accuracy
        plt.figure(figsize=(10, 6))
        plt.plot(sorted_categories, sorted_accuracies, marker='o', color='blue', label="Category-wise Accuracy")

        # Add the Overall Accuracy as a horizontal line
        plt.axhline(y=overall_accuracy, color='red', linestyle='--', label=f"Overall Accuracy: {overall_accuracy:.2f}%")

        # Add labels and title
        plt.ylim(0, 100)
        plt.xlabel(x_label)
        plt.ylabel('Accuracy (%)')
        plt.title('Category-wise Accuracy vs Overall Accuracy')
        plt.xticks(sorted_categories)  # Ensure all categories are shown on x-axis
        plt.legend()

        # Show the plot
        # plt.show()

        save_path = os.path.join(domain_name, output)
        plt.savefig(save_path)
        plt.close()


def plot_error_bars(data, domain_name, output, x_label='Grid Dimensions', bucket_size=1):
    overall_accuracy = data["Overall Accuracy"]
    category_accuracy = data["Category-wise Accuracy"]
    # category_counts = data["Category-wise Counts"]  # Assuming this contains the number of examples per category

    

    # Extract category names and accuracies
    categories = list(map(int, category_accuracy.keys()))  # Convert category keys to integers for proper plotting
    accuracies = np.array(list(category_accuracy.values())) / 100  # Convert to proportion for variance calculation

    num_categories = len(categories)
    directory_path = os.path.join(domain_name, 'data')
    num_files = len(os.listdir(directory_path))

    n = num_files // num_categories


    counts = np.array([n for cat in categories])  # Get counts for each category

    # Compute standard deviation (sqrt of variance)
    errors = 1.96*np.sqrt(accuracies * (1 - accuracies) / counts) * 100  # Convert back to percentage

    # Sort categories and corresponding values for proper plotting
    sorted_data = sorted(zip(categories, accuracies, errors))
    sorted_categories, sorted_accuracies, sorted_errors = zip(*sorted_data)

    # Plot Category-wise Accuracy with error bars
    plt.figure(figsize=(10, 6))
    plt.errorbar(sorted_categories, np.array(sorted_accuracies) * 100, yerr=sorted_errors, fmt='-o', capsize=5, 
                 capthick=2, elinewidth=1, color='blue', label="Category-wise Accuracy")

    # Add the Overall Accuracy as a horizontal line
    plt.axhline(y=overall_accuracy, color='red', linestyle='--', label=f"Overall Accuracy: {overall_accuracy:.2f}%")

    # Add labels and title
    plt.xlabel(x_label)
    plt.ylabel('Accuracy (%)')
    plt.title('Category-wise Accuracy vs Overall Accuracy')
    plt.xticks(sorted_categories)  # Ensure all categories are shown on x-axis
    plt.legend()

    # Save the plot
    save_path = os.path.join(domain_name, output)
    plt.savefig(save_path)
    plt.close()

# Function to plot the data
def plot_accuracy_few_shot(data, data_2 , domain_name , output, x_label = 'Grid Dimensions'):
    overall_accuracy = data["Overall Accuracy"]
    category_accuracy = data["Category-wise Accuracy"]
    overall_accuracy_2 = data_2["Overall Accuracy"]
    category_accuracy_2 = data_2["Category-wise Accuracy"]

    # Extract category names and accuracies
    categories = list(map(int,category_accuracy.keys()))  # Convert category keys to integers for proper plotting4
    accuracies = list(category_accuracy.values())

    # Sort categories and accuracies for proper plotting
    sorted_categories, sorted_accuracies = zip(*sorted(zip(categories, accuracies)))

   

    # Plot Category-wise Accuracy
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_categories, sorted_accuracies, marker='o', color='red', label="Category-wise Accuracy")

    #plot data drom data_2 on same graph
    categories_2 = list(map(int,category_accuracy_2.keys()))  # Convert category keys to integers for proper plotting
    accuracies_2 = list(category_accuracy_2.values())

    # Sort categories and accuracies for proper plotting
    sorted_categories_2, sorted_accuracies_2 = zip(*sorted(zip(categories_2, accuracies_2)))

    plt.plot(sorted_categories_2, sorted_accuracies_2, marker='o', color='blue', label="Category-wise Accuracy Few Shot")

    # Add the Overall Accuracy as a horizontal line
    plt.axhline(y=overall_accuracy, color='red', linestyle='--', label=f"Overall Accuracy: {overall_accuracy:.2f}%")
    plt.axhline(y=overall_accuracy_2, color='blue', linestyle='--', label=f"Overall Accuracy Few Shot: {overall_accuracy_2:.2f}%")

    # Add labels and title
    plt.xlabel(x_label)
    plt.ylabel('Accuracy (%)')
    plt.title('Category-wise Accuracy vs Overall Accuracy')
    plt.xticks(sorted_categories)  # Ensure all categories are shown on x-axis
    plt.legend()

    # Show the plot
    # plt.show()

    save_path = os.path.join(domain_name, output)
    plt.savefig(save_path)
    plt.close()
    # plt.show()

def plot_accuracy_ind(data, data_2 , data_3 , domain_name , output, x_label = 'Grid Dimensions'):
    overall_accuracy = data["Overall Accuracy"]
    category_accuracy = data["Category-wise Accuracy"]
    overall_accuracy_2 = data_2["Overall Accuracy"]
    category_accuracy_2 = data_2["Category-wise Accuracy"]
    overall_accuracy_3 = data_3["Overall Accuracy"]
    category_accuracy_3 = data_3["Category-wise Accuracy"]

    # Extract category names and accuracies
    categories = list(map(int,category_accuracy.keys()))  # Convert category keys to integers for proper plotting4
    accuracies = list(category_accuracy.values())

    # Sort categories and accuracies for proper plotting
    sorted_categories, sorted_accuracies = zip(*sorted(zip(categories, accuracies)))

   

    # Plot Category-wise Accuracy
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_categories, sorted_accuracies, marker='o', color='red', label="Category-wise Accuracy")

    #plot data drom data_2 on same graph
    categories_2 = list(map(int,category_accuracy_2.keys()))  # Convert category keys to integers for proper plotting
    accuracies_2 = list(category_accuracy_2.values())

    # Sort categories and accuracies for proper plotting
    sorted_categories_2, sorted_accuracies_2 = zip(*sorted(zip(categories_2, accuracies_2)))

    plt.plot(sorted_categories_2, sorted_accuracies_2, marker='o', color='blue', label="Category-wise Accuracy Few Shot")

    #plot data drom data_3 on same graph
    categories_3 = list(map(int,category_accuracy_3.keys()))  # Convert category keys to integers for proper plotting
    accuracies_3 = list(category_accuracy_3.values())

    # Sort categories and accuracies for proper plotting
    sorted_categories_3, sorted_accuracies_3 = zip(*sorted(zip(categories_3, accuracies_3)))

    plt.plot(sorted_categories_3, sorted_accuracies_3, marker='o', color='green', label="Category-wise Accuracy Inductive")

    # Add the Overall Accuracy as a horizontal line
    plt.axhline(y=overall_accuracy, color='red', linestyle='--', label=f"Overall Accuracy: {overall_accuracy:.2f}%")
    plt.axhline(y=overall_accuracy_2, color='blue', linestyle='--', label=f"Overall Accuracy Few Shot: {overall_accuracy_2:.2f}%")
    plt.axhline(y=overall_accuracy_3, color='green', linestyle='--', label=f"Overall Accuracy Inductive: {overall_accuracy_3:.2f}%")

    # Add labels and title
    plt.xlabel(x_label)
    plt.ylabel('Accuracy (%)')
    plt.title('Category-wise Accuracy vs Overall Accuracy')
    plt.xticks(sorted_categories)  # Ensure all categories are shown on x-axis
    plt.legend()

    # Show the plot
    # plt.show()

    save_path = os.path.join(domain_name, output)
    plt.savefig(save_path)
    plt.close()

def plot_accuracy_multi(data, data_2 , domain_name , output,  x_label = 'Grid Dimensions' ):
    overall_accuracy = data["Overall Accuracy"]
    category_accuracy = data["Category-wise Accuracy"]
    overall_accuracy_2 = data_2["Overall Accuracy"]
    category_accuracy_2 = data_2["Category-wise Accuracy"]

    # Extract category names and accuracies
    categories = list(map(int,category_accuracy.keys()))  # Convert category keys to integers for proper plotting4
    accuracies = list(category_accuracy.values())

    # Sort categories and accuracies for proper plotting
    sorted_categories, sorted_accuracies = zip(*sorted(zip(categories, accuracies)))

   

    # Plot Category-wise Accuracy
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_categories, sorted_accuracies, marker='o', color='red', label="Category-wise Accuracy GPT")

    #plot data drom data_2 on same graph
    categories_2 = list(map(int,category_accuracy_2.keys()))  # Convert category keys to integers for proper plotting
    accuracies_2 = list(category_accuracy_2.values())

    # Sort categories and accuracies for proper plotting
    sorted_categories_2, sorted_accuracies_2 = zip(*sorted(zip(categories_2, accuracies_2)))

    plt.plot(sorted_categories_2, sorted_accuracies_2, marker='o', color='blue', label="Category-wise Accuracy Gemini")

    # Add the Overall Accuracy as a horizontal line
    plt.axhline(y=overall_accuracy, color='red', linestyle='--', label=f"Overall Accuracy: {overall_accuracy:.2f}%")
    plt.axhline(y=overall_accuracy_2, color='blue', linestyle='--', label=f"Overall Accuracy Multi Agent: {overall_accuracy_2:.2f}%")

    # Add labels and title
    plt.xlabel(x_label)
    plt.ylabel('Accuracy (%)')
    plt.title('Category-wise Accuracy vs Overall Accuracy')
    plt.xticks(sorted_categories)  # Ensure all categories are shown on x-axis
    plt.legend()

    # Show the plot
    # plt.show()

    save_path = os.path.join(domain_name, output)
    plt.savefig(save_path)
    plt.close()
    # plt.show()

def accuracy_overall(domain, models):
    for model in models:
        data = read_data(os.path.join(domain, 'eval_'+model+'.json'))
        category_accuracy = data["Category-wise Accuracy"]
        categories = list(map(int,category_accuracy.keys()))  # Convert category keys to integers for proper plotting4
        accuracies = list(category_accuracy.values())
        plt.plot(categories, accuracies, marker='o')
    plt.ylim(-10, 110)
    plt.xlabel(x_label)
    plt.ylabel('Accuracy (%)')
    plt.title('Overall Accuracy')
    plt.xticks(sorted(categories))  # Ensure all categories are shown on x-axis
    plt.legend(models)
    #plt.legend()

    # Show the plot
    # plt.show()

    save_path = os.path.join(domain, 'accuracy_overall.png')
    plt.savefig(save_path)
    plt.close()

# Main function to execute the script
if __name__ == "__main__":

    
    # Path to the JSON file (replace with your file path)
    # file_path = 'data.json'
    
    # domain_name = sys.argv[1]

    # file_path = os.path.join(domain_name, 'eval.json')
    # # Read the data
    # data = read_data(file_path)

    # # Plot the accuracy graph
    # plot_accuracy(data , domain_name)

    parser = argparse.ArgumentParser(description='Create the eval graph of a domain')

    parser.add_argument(
        '--domain_name',
        '-d',
        type=str,
        help='Name of the domain',
        required=True
    )
    parser.add_argument(
        '--x_label',
        '-x',
        type=str,
        help='Name of the x-axis label',
        default='Number of Items'
    )
    parser.add_argument(
        '--type',
        '-t',
        type=str,
        help='Type of the prompting',
        default='zero'
    )
    parser.add_argument(
        '--bucket_size',
        '-b',
        type=int,
        help='Size of the bucket for grouping categories',
        default = 1
    )
    parser.add_argument(
        '--eval',
        '-e',
        type=str,
        help='Name of eval file',
        default='eval.json'
    )
    parser.add_argument(
        '--image',
        '-i',
        type=str,
        help='Name of image file',
        default='accuracy_graph.png'
    )
    args = parser.parse_args()
    type = args.type
    domain_name = args.domain_name
    x_label = args.x_label
    bucket_size = args.bucket_size

    if type == 'few':

        file_path = os.path.join(domain_name, 'eval.json')
    # Read the data
        data = read_data(file_path)

        file_path_2 = os.path.join(domain_name, 'eval_few_shot.json')
        data_2 = read_data(file_path_2)
        # Plot the accuracy graph
        plot_accuracy_few_shot(data , data_2 , domain_name , args.image, x_label)    

    elif type == 'inductive':

        file_path = os.path.join(domain_name, 'eval.json')
    # Read the data
        data = read_data(file_path)

        file_path_2 = os.path.join(domain_name, 'eval_few_shot.json')
        data_2 = read_data(file_path_2)
        # Plot the accuracy graph

        file_path_3 = os.path.join(domain_name, 'eval_inductive.json')
        data_3 = read_data(file_path_3)

        plot_accuracy_ind(data , data_2, data_3, domain_name , args.image, x_label)  

    elif type == 'multi':
        file_path = os.path.join(domain_name, 'eval.json')
        # Read the data
        data = read_data(file_path)
        file_path_2 = os.path.join(domain_name, 'eval_gemini.json')
        data_2 = read_data(file_path_2)
        plot_accuracy_multi(data , data_2 , domain_name , args.image, x_label)

    elif type == 'error':
        
        file_path = os.path.join(domain_name, args.eval)
        # Read the data
        data = read_data(file_path)

        # Plot the accuracy graph
        plot_error_bars(data , domain_name , args.image, x_label , bucket_size=bucket_size)

    elif type == 'overall':
        models = ['gpt-4o', 'o4-mini', 'gemini', 'qwen', 'deepseek']
        accuracy_overall(args.domain_name, models)

    else:

        file_path = os.path.join(domain_name, args.eval)
        # Read the data
        data = read_data(file_path)

        # Plot the accuracy graph

        plot_accuracy(data , domain_name , args.image, x_label , bucket_size=bucket_size)  
