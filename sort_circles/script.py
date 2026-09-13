import matplotlib.pyplot as plt
import random
import os
import json
import argparse

def generate_circles(num_circles, min_size_diff=0.05):
    # Create a figure
    global file
    fig, ax = plt.subplots(figsize=(num_circles * 3, 5))

    # Data to store the circles' information
    circles_info = []
    
    # X-axis positions to ensure the circles are aligned horizontally
    x_position = 0

    # Store previously generated sizes to ensure minimum difference between sizes
    radii = [0]
    
    for i in range(1, num_circles + 1):
        # Generate a random radius ensuring no two are too close in size
        while True:
            radius = random.uniform(0.3, 2)  # Random size for the circle
            if all(abs(radius - r) >= min_size_diff for r in radii):
                radii.append(radius)
                break

        x_position += radius + radii[-2] + 0.5  # X-position for the circle
        y = 2  # Y-position for alignment (all circles in a line)
        
        # Plot the circle
        circle = plt.Circle((x_position, y), radius, color='black', fill=True)
        ax.add_patch(circle)
        
        # Label the circle
        ax.text(x_position, y, f'{i}', ha='center', va='center', fontsize=24, color='white')
        
        # Store the circle's label and size
        circles_info.append({'label': i , 'size': radius})
    
    # Set limits and hide axes
    ax.set_xlim(0, x_position + 2)
    ax.set_ylim(0, 4)
    ax.set_aspect('equal')
    ax.axis('off')
    
    image_filename = f"{file}.png"
    image_path = os.path.join(output_dir, image_filename)
    plt.savefig(image_path, bbox_inches='tight')
    plt.close(fig)

    return circles_info

def sort_circles(circles_info):
    # Sort the circles based on their size
    sorted_circles = sorted(circles_info, key=lambda x: x['size'])
    
    # Print the gold output
    # print("Gold output (sorted by size):")
    # for circle in sorted_circles:
    #     print(f"{circle['label']}: Size {circle['size']:.2f}")
    
    return sorted_circles

# def main():
#     num_circles = 5  # Specify the number of circles to generate
#     circles_info = generate_circles(num_circles)  # Generate the circles and store their info
    
#     # Sort the circles by size and get the gold output
#     gold_output = sort_circles(circles_info)


    
#     return gold_output
    # Optionally, you can save this output to a file or use it for further processing

if __name__ == "__main__":
    output_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)    
    # file = 1
    # num_images = int(sys.argv[1])
    # num_object_list = sys.argv[2:]
    # num_object_list = [int(num_objects) for num_objects in num_object_list]
    parser = argparse.ArgumentParser(description='Create a grid of circles and triangles.')
    parser.add_argument(
        '--num_images', 
        type=int, 
        help='Number of images to generate',
        default=1
    )
    parser.add_argument(
        '--num_sizes', 
        nargs='*', 
        help='List of n values',
        type=int,
        default=[5 , 3]
    )
    parser.add_argument(
        '--file', 
        type=int, 
        help='Starting file number',
        default=1
    )
    args = parser.parse_args()
    file = args.file
    num_object_list = args.num_sizes
    num_images = args.num_images
    append = (file != 1)
    data = []
    # main()/
    for num_circles in num_object_list:
        for _ in range(num_images):
            circles_info = generate_circles(num_circles)
            output = sort_circles(circles_info)
            # Store the number of objects in the image_data dictionary
            gold_output = [circle['label'] for circle in output]
            gold_output = {
                "id": f'{file}.png',
                "Gold_output": gold_output,
                "Rows" : num_circles
            }
            file += 1
            data.append(gold_output)

    if append:
        with open(os.path.join(os.getcwd() , "data.json"), "r") as f:
            old_data = json.load(f)
            old_data.extend(data)
        with open(os.path.join(os.getcwd() , "data.json"), "w") as f:
            json.dump(old_data, f, indent=2)
    else:
        with open(os.path.join(os.getcwd() , "data.json"), "w") as f:
            json.dump(data, f, indent=2)
