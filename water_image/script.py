import matplotlib.pyplot as plt
import cv2
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
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data = []
    append = (file != 1)

    for n in num_objects_list:
        max_obj = 2*n
        for img_index in range(num_images):
            """fig, ax = plt.subplots()
            ax.set_aspect('equal')
            plt.axis('off')

            # Adjust plot limits to prevent cutoff
            plt.xlim(-0.1, 1.1)
            plt.ylim(-0.1, 1.1)

            # Generate random positions for the shapes
            positions = []
            radius = 0.05
            shapes = ['circle', 'triangle', 'rectangle', 'pentagon']
            colours = ['red', 'green', 'blue', 'yellow', 'orange', 'black']
            for i in range(n):
                while True:
                    x, y = random.uniform(0.1, 0.9), random.uniform(0.1, 0.9)
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

                if shape_type == 'circle':
                    shape = plt.Circle((x, y), radius, color=color)
                elif shape_type == 'triangle':
                    triangle = np.array([[x, y + radius], [x - radius, y - radius], [x + radius, y - radius]])
                    shape = plt.Polygon(triangle, color=color)
                elif shape_type == 'rectangle':
                    shape = plt.Rectangle((x - radius, y - radius), 2 * radius, 2 * radius, color=color)
                elif shape_type == 'pentagon':
                    pentagon = np.array([
                        [x, y + radius], [x + 0.95 * radius, y + 0.31 * radius],
                        [x + 0.59 * radius, y - 0.81 * radius], [x - 0.59 * radius, y - 0.81 * radius],
                        [x - 0.95 * radius, y + 0.31 * radius]
                    ])
                    shape = plt.Polygon(pentagon, color=color)

                ax.add_patch(shape)"""
                #ax.text(x, y, str(i + 1), color='white', ha='center', va='center', fontsize=8, weight='bold')

            # Save the plot to a file
            fig, ax = plt.subplots()
            ax.set_aspect('equal')
            plt.axis('off')

            # Adjust plot limits to prevent cutoff
            plt.xlim(-203.5, 203.5)
            plt.ylim(-203.5, 203.5)

            # Generate random positions for the shapes
            positions = []
            radius = 3.5
            shapes = ['circle', 'triangle', 'rectangle', 'pentagon']
            colours = ['red', 'green', 'blue', 'yellow', 'orange', 'black']
            for i in range(max_obj):
                while True:
                    x, y = random.uniform(-200, 200), random.uniform(3.5, 200)
                    # Ensure shapes don't overlap
                    if all(((x - px) ** 2 + (y - py) ** 2) ** 0.5 > 2 * radius for px, py in positions):
                        positions.append((x, y))
                        break

            # Choose one odd-colored shape
            #odd_index = random.randint(0, n - 1)

            # Draw shapes and label them
            color, shape_type = [], []
            plt.axhline(y = 0, color = 'blue')
            for i, (x, y) in enumerate(positions):
                color.append(random.choice(colours))
                shape_type.append(random.choice(shapes))

                if shape_type[-1] == 'circle':
                    shape = plt.Circle((x, y), radius, color=color[-1])
                elif shape_type[-1] == 'triangle':
                    triangle = np.array([[x, y + radius], [x - radius, y - radius], [x + radius, y - radius]])
                    shape = plt.Polygon(triangle, color=color[-1])
                elif shape_type[-1] == 'rectangle':
                    shape = plt.Rectangle((x - radius, y - radius), 2 * radius, 2 * radius, color=color[-1])
                elif shape_type[-1] == 'pentagon':
                    pentagon = np.array([
                        [x, y + radius], [x + 0.95 * radius, y + 0.31 * radius],
                        [x + 0.59 * radius, y - 0.81 * radius], [x - 0.59 * radius, y - 0.81 * radius],
                        [x - 0.95 * radius, y + 0.31 * radius]
                    ])
                    shape = plt.Polygon(pentagon, color=color[-1])

                ax.add_patch(shape)
            filename = f"first{file}.png"
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath, bbox_inches='tight')
            plt.close()

            fig, ax = plt.subplots()
            ax.set_aspect('equal')
            plt.axis('off')

            # Adjust plot limits to prevent cutoff
            plt.xlim(-203.5, 203.5)
            plt.ylim(-203.5, 203.5)

            for i in range(n):
                x = list(positions[i])
                x[1] = -x[1]
                positions[i] = tuple(x)

            plt.axhline(y = 0, color = 'blue')
            for i, (x, y) in enumerate(positions):
                if shape_type[i] == 'circle':
                    shape = plt.Circle((x, y), radius, color=color[i])
                elif shape_type[i] == 'triangle':
                    triangle = np.array([[x, y + radius], [x - radius, y - radius], [x + radius, y - radius]])
                    shape = plt.Polygon(triangle, color=color[i])
                elif shape_type[i] == 'rectangle':
                    shape = plt.Rectangle((x - radius, y - radius), 2 * radius, 2 * radius, color=color[i])
                elif shape_type[i] == 'pentagon':
                    pentagon = np.array([
                        [x, y + radius], [x + 0.95 * radius, y + 0.31 * radius],
                        [x + 0.59 * radius, y - 0.81 * radius], [x - 0.59 * radius, y - 0.81 * radius],
                        [x - 0.95 * radius, y + 0.31 * radius]
                    ])
                    shape = plt.Polygon(pentagon, color=color[i])

                ax.add_patch(shape)
            filename = f"second{file}.png"
            file += 1
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath, bbox_inches='tight')
            plt.close()
            
            gold_answer = n
            """if choice == 0:
                img = cv2.imread(filepath)
                img_mirror = np.flip(img, axis=1)
                cv2.imwrite(os.path.join(output_dir, f"second{file-1}.png"), img_mirror)
                gold_answer = "Yes"
            else:
                angles = [90, 180, 270, 360]
                angle = random.choice(angles)
                img = Image.open(filepath)
                rotated_image = img.rotate(angle, PIL.Image.BILINEAR)
                rotated_image.save(os.path.join(output_dir, f"second{file-1}.png"), "PNG")
                gold_answer = "No"
                
            """


            gold_output = {
                "id": filename,
                "water_image": gold_answer,
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
