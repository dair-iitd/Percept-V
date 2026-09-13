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
            #im = Image.open(os.path.join(input_dir, f"bg_{img_index+1}.png"))
            fig, ax = plt.subplots()
            #ax.imshow(im)
            ax.set_aspect('equal')
            plt.axis('off')

            # Adjust plot limits to prevent cutoff
            plt.xlim(-1500.0, 1500.0)
            plt.ylim(-1000, 1000)

            # Generate random positions for the shapes
            positions = []
            radius = 75
            height, width = 1000, 1500
        
            for i in range(n):
                while True:
                    x, y = random.randint(-(width - radius), (width - radius)), random.randint(-(height - radius), (height-radius))
                    # Ensure shapes don't overlap
                    if all(((x - px) ** 2 + (y - py) ** 2) ** 0.5 > 2 * radius for px, py in positions) and (abs(x) > radius and abs(y) > radius):
                        positions.append((x, y))
                        break

            # Draw shapes and label them
            first, second, third, fourth = 0, 0, 0, 0
            plt.axhline(0, color='black', linewidth=0.5)
            plt.axvline(0, color='black', linewidth=0.5)

            for i, (x, y) in enumerate(positions):
                #color = random.choice(colours)
                #shape_type = random.choice(shapes)
                if x>0 and y>0:
                    first += 1
                elif x<0 and y>0:
                    second += 1
                elif x<0 and y<0:
                    third += 1
                else:
                    fourth += 1

                shape = plt.Circle((x, y), radius, color='black')
                ax.add_patch(shape)
                #ax.text(x, y, str(i + 1), color='white', ha='center', va='center', fontsize=8, weight='bold')

            # Save the plot to a file
            filename = f"{file}.png"
            file += 1
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath, bbox_inches='tight')
            plt.close()
            iterable = [first, second, third, fourth]
            answer = max(enumerate(iterable), key=lambda x: x[1])[0] + 1

            gold_output = {
                "id": filename,
                "quadrant": answer,
                "count": iterable[answer-1],
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
