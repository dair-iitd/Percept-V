import matplotlib.pyplot as plt
from itertools import combinations
import cv2
import random
import os
import json
import argparse
import numpy as np



def generate_depth_images(num_images , num_object_list , file , image_size=(500, 500)):
    output_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data = []
    append = (file != 1)

    for n in num_object_list:
        for _ in range(num_images):  
            colors = {'black', 'gray', 'brown', 'maroon', 'red', 'coral', 'tan', 'orange', 'ivory', 'goldenrod', 'yellow', 'green', 'olive', 'turquoise', 'skyblue', 'blue', 'lavender', 'purple', 'pink', 'fuchsia'}
            colors_n = random.choice(list(combinations(colors, n)))
            #print(colors_n)
            random.shuffle(list(colors_n))
            
            fig, ax = plt.subplots()
            ax.set_aspect('equal')
            plt.axis('off')

            # Adjust plot limits to prevent cutoff
            plt.xlim(-1.0, 1.0)
            plt.ylim(-1.0, 1.0)

            # Generate random positions for the shapes
            radii = np.linspace(0.9, 0.05, n)

            # Draw shapes and label them
            cx, cy = 0.0, 0.0
            for i in range(n):
                shape = plt.Circle((cx, cy), radii[i], color=colors_n[i], ec='black', fill=True)
                ax.add_patch(shape)

            # Save the plot to a file
            filename = f"{file}.png"
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath, bbox_inches='tight')
            plt.close()

            img1 = cv2.imread("data/"+f"{file}.png")
            img2 = cv2.imread("swatches.png")
            if img1.shape[1] != img2.shape[1]:
                max_width = max(img1.shape[1], img2.shape[1])
                img1 = cv2.resize(img1, (max_width, img1.shape[0]))
                img2 = cv2.resize(img2, (max_width, img2.shape[0]))

            merged_image = cv2.vconcat([img1, img2])
            cv2.imwrite(filepath, merged_image)
            file += 1

            gold_output = {
                "id": filename,
                "num_layers" : n,
                "colors": colors_n[::-1],    
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
            

# # Generate and display an example image
# n_shapes = 3
# image = generate_depth_images(n_shapes)
# image.show()

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
        help='List of count of layers',
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
    generate_depth_images(args.num_images, num_object_list , file)
