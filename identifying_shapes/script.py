import matplotlib.pyplot as plt
import matplotlib.patches as mp
import random
import os
import json
import sys
import argparse


def create_images(num_images, num_objects_list, items_list):
    # Ensure the output directory exists
    output_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data = []
    
    file = 1
    for num_objects in num_objects_list:
        dpi = 100  # Dots per inch
        width_inches = 1  # 100 pixels
        height_inches = num_objects  # 100 pixels per row
        for img_index in range(num_images):
            fig, ax = plt.subplots(figsize=(width_inches, height_inches), dpi=dpi)
            image_data = []
            image_side = []
            for i in range (num_objects):
                shape, sides = random.choice(list(items_list.items()))
                y = num_objects - i - 1 
                image_data.append(shape)
                image_side.append(sides)
                # Ensure the circles do not overlap by adjusting positions
                # Add circles to the plot
                if(shape == 'Circle'):
                    circle = mp.Circle((0.5, y), 0.3, color='blue', fill=True)
                    ax.add_patch(circle)
                if(shape == 'Diamond'):
                    sq = mp.RegularPolygon((0.5, y), numVertices=4, radius=0.3, facecolor='green')
                    ax.add_patch(sq)
                if(shape == 'Triangle'):
                    tri = mp.RegularPolygon((0.5, y), numVertices=3, radius=0.3, facecolor='red')
                    ax.add_patch(tri)
                if(shape == 'Pentagon'):
                    pent = mp.RegularPolygon((0.5, y), numVertices=5, radius=0.3, facecolor='cyan')
                    ax.add_patch(pent)
                if(shape == 'Hexagon'):
                    hex = mp.RegularPolygon((0.5, y), numVertices=6, radius=0.3, facecolor='magenta')
                    ax.add_patch(hex)

                if i < num_objects -1:
                    ax.plot([0, 1], [y - 0.5, y - 0.5], color='black')

            ax.set_xlim(0, 1)
            ax.set_ylim(-0.5, num_objects - 0.5)
            ax.set_aspect('equal')
            ax.axis('off')

            image_filename = f"{file}.png"
            file += 1
            image_path = os.path.join(output_dir, image_filename)
            plt.savefig(image_path, bbox_inches='tight', dpi=dpi)
            plt.close(fig)
            
            

            # Store the number of objects in the image_data dictionary
            gold_output = {
                "id": image_filename,
                "Gold_output": image_data,
                "Gold_side": image_side,
                "Rows" : num_objects
            }
            data.append(gold_output)

    # Save the data to a JSON file
    with open(os.path.join(os.getcwd() , "data.json"), "w") as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    # Parse command line arguments
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
        help='List of count of circles',
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
    items_list = {'Circle':0, 'Triangle':3, 'Diamond':4, 'Pentagon':5, 'Hexagon':6}
    create_images(args.num_images, num_object_list, items_list)
    # print(num_object_list)
    # Create images with the specified number of objects