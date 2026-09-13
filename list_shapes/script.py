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
            im = Image.open(os.path.join(input_dir, f"bg_{img_index+1}.png"))
            fig, ax = plt.subplots()
            ax.imshow(im)
            ax.set_aspect('equal')
            plt.axis('off')

            # Adjust plot limits to prevent cutoff
            #plt.xlim(-1500.0, 1500.0)
            #plt.ylim(-1000, 1000)

            # Generate random positions for the shapes
            positions = []
            radius = 75
            shapes = ['circle', 'triangle', 'square', 'pentagon']
            colours = ['red', 'green', 'blue']
            height, width = im.size
            gold_answer = set()
            for i in range(n):
                while True:
                    x, y = random.randint(2*radius, height-(2*radius)), random.randint(2*radius, width-(2*radius))
                    # Ensure shapes don't overlap
                    if all(((x - px) ** 2 + (y - py) ** 2) ** 0.5 > 2 * radius for px, py in positions):
                        positions.append((x, y))
                        break

            # Choose one odd-colored shape
            #odd_index = random.randint(0, n - 1)

            # Draw shapes and label them
            for i, (x, y) in enumerate(positions):
                color = random.choice(colours)
                shape_type = random.choice(shapes)
                gold_answer.add(shape_type)

                if shape_type == 'circle':
                    shape = plt.Circle((x, y), radius, color=color)
                elif shape_type == 'triangle':
                    triangle = np.array([[x, y + radius], [x - radius, y - radius], [x + radius, y - radius]])
                    shape = plt.Polygon(triangle, color=color)
                elif shape_type == 'square':
                    shape = plt.Rectangle((x - radius, y - radius), 2 * radius, 2 * radius, color=color)
                elif shape_type == 'pentagon':
                    pentagon = np.array([
                        [x, y + radius], [x + 0.95 * radius, y + 0.31 * radius],
                        [x + 0.59 * radius, y - 0.81 * radius], [x - 0.59 * radius, y - 0.81 * radius],
                        [x - 0.95 * radius, y + 0.31 * radius]
                    ])
                    shape = plt.Polygon(pentagon, color=color)

                ax.add_patch(shape)
                #ax.text(x, y, str(i + 1), color='white', ha='center', va='center', fontsize=8, weight='bold')

            # Save the plot to a file
            filename = f"{file}.png"
            file += 1
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath, bbox_inches='tight')
            plt.close()
            answer = sorted(list(gold_answer))

            gold_output = {
                "id": filename,
                "list_shapes": answer,
                "num_objects": n
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
