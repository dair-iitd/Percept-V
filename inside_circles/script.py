import matplotlib.pyplot as plt
import PIL
from PIL import Image
import random
import numpy as np
import os
import json
import argparse

def generate_shapes(num_images, num_objects_list , file):
    # Set up the plot

    output_dir = os.path.join(os.getcwd(), "data")
    input_dir = os.path.join(os.getcwd(), "background_image")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data = []
    append = (file != 1)

    for n in num_objects_list:
        for img_index in range(num_images):
            fig, ax = plt.subplots()
            ax.set_aspect('equal')
            plt.axis('off')

            # Adjust plot limits to prevent cutoff
            plt.xlim(-0.7, 1.4)
            plt.ylim(-0.7, 1.4)

            # Generate random positions for the shapes
            positions = []
            radii = []
            gold_answer = 0
            for i in range(n):
                x, y = random.uniform(0.1, 0.9), random.uniform(0.1, 0.9)
                positions.append((x, y))
                radius = random.uniform(0.1, 0.5)
                radii.append(radius)

            # Draw shapes and label them
            cx, cy = random.uniform(0.1, 0.9), random.uniform(0.1, 0.9)
            ax.add_patch(plt.Circle((cx, cy), 0.05, color='red'))
            for i, (x, y) in enumerate(positions):
                shape = plt.Circle((x, y), radii[i], color='black', fill=False)
                ax.add_patch(shape)
                
                if ((cx - x)**2 + (cy - y)**2)**0.5 < radii[i]:
                    gold_answer += 1

            # Save the plot to a file
            filename = f"{file}.png"
            file += 1
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath, bbox_inches='tight')
            plt.close()
            answer = False
            if gold_answer == 0:
                answer = False
            else:
                answer = True

            gold_output = {
                "id": filename,
                "inside_circles": answer,
                "num_circles": n
            }
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



# # Example usage
# generate_shapes(10, 'shapes.png')
if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Create an image of different objects')
    parser.add_argument(
        '--num_images', 
        type=int, 
        help='Number of images to generate',
        default=1
    )
    parser.add_argument(
        '--num_sizes', 
        nargs='*', 
        type=int,
        help='List of count of objects',
        default=[5]
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
    append = (file != 1)
    generate_shapes(args.num_images, num_object_list , file)
