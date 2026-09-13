import matplotlib.pyplot as plt
import numpy as np
import random
import os
import json
import argparse

def create_images(num_images, num_objects_list , file):
    # Ensure the output directory exists
    output_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data = []
    
    append = (file != 1)
    for num_objects in num_objects_list:
        dpi = 100  # Dots per inch
        width_inches = 1  # 100 pixels
        height_inches = num_objects + 1  # 100 pixels per row
        for img_index in range(num_images):
            shapes1, shapes2 = [], []
            fig, ax = plt.subplots(figsize=(width_inches, height_inches), dpi=dpi)
            for i in range (num_objects):
                y = num_objects - i - 1
                x = 0.5
                radius = 0.1
                shapes = ['circle', 'triangle', 'rectangle', 'pentagon']
                #colours = ['red', 'green', 'blue']


                # Add circles to the plot
                shape_type = random.choice(shapes)
                shapes1.append(shape_type)
                if shape_type == 'circle':
                    shape = plt.Circle((x, y), radius, color="blue")
                elif shape_type == 'triangle':
                    triangle = np.array([[x, y + radius], [x - radius, y - radius], [x + radius, y - radius]])
                    shape = plt.Polygon(triangle, color="blue")
                elif shape_type == 'rectangle':
                    shape = plt.Rectangle((x - radius, y - radius), 2 * radius, 2 * radius, color="blue")
                elif shape_type == 'pentagon':
                    pentagon = np.array([
                        [x, y + radius], [x + 0.95 * radius, y + 0.31 * radius],
                        [x + 0.59 * radius, y - 0.81 * radius], [x - 0.59 * radius, y - 0.81 * radius],
                        [x - 0.95 * radius, y + 0.31 * radius]
                    ])
                    shape = plt.Polygon(pentagon, color="blue")
                ax.add_patch(shape)

                # if i < num_objects -1:
                ax.plot([0, 1], [y - 0.5, y - 0.5], color='black')

            ax.set_xlim(0, 1)
            ax.set_ylim(-0.6, num_objects - 0.5)
            ax.set_aspect('equal')
            ax.axis('off')

            image_filename = f"first{file}.png"
            image_path = os.path.join(output_dir, image_filename)
            plt.savefig(image_path, bbox_inches='tight', dpi=dpi)
            plt.close(fig)

            fig, ax = plt.subplots(figsize=(width_inches, height_inches), dpi=dpi)
            for i in range (num_objects):
                y = num_objects - i - 1
                x = 0.5
                radius = 0.1
                shapes = ['circle', 'triangle', 'rectangle', 'pentagon']
                #colours = ['red', 'green', 'blue']


                # Add circles to the plot
                shape_type = random.choice(shapes)
                shapes2.append(shape_type)
                if shape_type == 'circle':
                    shape = plt.Circle((x, y), radius, color="blue")
                elif shape_type == 'triangle':
                    triangle = np.array([[x, y - radius], [x - radius, y + radius], [x + radius, y + radius]])
                    shape = plt.Polygon(triangle, color="blue")
                elif shape_type == 'rectangle':
                    shape = plt.Rectangle((x - radius, y - radius), 2 * radius, 2 * radius, color="blue")
                elif shape_type == 'pentagon':
                    pentagon = np.array([
                        [x, y - radius], [x + 0.95 * radius, y - 0.31 * radius],
                        [x + 0.59 * radius, y + 0.81 * radius], [x - 0.59 * radius, y + 0.81 * radius],
                        [x - 0.95 * radius, y - 0.31 * radius]
                    ])
                    shape = plt.Polygon(pentagon, color="blue")
                ax.add_patch(shape)

                # if i < num_objects -1:
                ax.plot([0, 1], [y - 0.5, y - 0.5], color='black')

            ax.set_xlim(0, 1)
            ax.set_ylim(-0.6, num_objects - 0.5)
            ax.set_aspect('equal')
            ax.axis('off')

            image_filename = f"second{file}.png"
            file += 1
            image_path = os.path.join(output_dir, image_filename)
            plt.savefig(image_path, bbox_inches='tight', dpi=dpi)
            plt.close(fig)

            answer = 0
            for i in range(num_objects):
                if(shapes1[i] == shapes2[i]):
                    answer += 1
            
            

            # Store the number of objects in the image_data dictionary
            gold_output = {
                "id": image_filename,
                "Gold_output": answer,
                "Rows" : num_objects
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

if __name__ == "__main__":
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
        type=int,
        help='List of number of rows',
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
    create_images(args.num_images, num_object_list , file)
