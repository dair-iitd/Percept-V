import matplotlib.pyplot as plt
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
            fig, ax = plt.subplots(figsize=(width_inches, height_inches), dpi=dpi)
            image_data = []
            for i in range (num_objects):
                y = num_objects - i - 1 
                while True:
                    radius1 = random.uniform(0.05, 0.2)
                    radius2 = random.uniform(0.05, 0.2)
                    if abs(radius1 - radius2) >= 0.05:
                        break

                if radius1 > radius2:
                    image_data.append("Blue")
                else:
                    image_data.append("Green")
                # Ensure the circles do not overlap by adjusting positions
                x1, x2 = 0.25, 0.75

                # Add circles to the plot
                circle1 = plt.Circle((x1, y), radius1, color='blue', fill=True)
                circle2 = plt.Circle((x2, y), radius2, color='green', fill=True)
                ax.add_patch(circle1)
                ax.add_patch(circle2)

                # if i < num_objects -1:
                ax.plot([0, 1], [y - 0.5, y - 0.5], color='black')

            ax.set_xlim(0, 1)
            ax.set_ylim(-0.6, num_objects - 0.5)
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
