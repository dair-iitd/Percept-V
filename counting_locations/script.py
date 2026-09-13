import os
import json
from PIL import Image, ImageDraw
import random
import argparse

# Function to draw an object
def draw_object(draw, position, color):
    x, y = position
    size = 30
    draw.ellipse([x, y, x + size, y + size], fill=color)

def create_images(num_images, num_objects_list , file):
    append = (file != 1)
    data = []
    for num_objects in num_objects_list:
        print(f"Creating {num_images} images with {num_objects} objects...")
        max_obj = 2*num_objects
        for i in range(num_images):
            # Image dimensions
            width, height = 500, 300

            # Create a blank image with a white background
            image = Image.new("RGB", (width, height), "white")
            draw = ImageDraw.Draw(image)

            # Draw a simple table (a rectangle)
            table_top_left = (10, 140)
            table_bottom_right = (width-10, 160)
            draw.rectangle([table_top_left, table_bottom_right], fill="brown")

            # Randomly generate positions for objects
            positions = []
            num_over_table = 0
            num_under_table = 0
            for i in range(max_obj):
                while True:
                    # Randomly decide whether the object is over or under the table
                    if i < num_objects:
                        # Over the table (above the table's top edge)
                        x = random.randint(10, width - 30)
                        y = random.randint(0, table_top_left[1] - 40)
                        if not any(abs(x - px) < 35 and abs(y - py) < 35 for px, py in positions):
                            positions.append((x, y))
                            num_over_table += 1
                            break
                        
                    else:
                        # Under the table (below the table's bottom edge)
                        x = random.randint(10, width - 30)
                        y = random.randint(table_bottom_right[1] + 10, height - 40)
                        if not any(abs(x - px) < 35 and abs(y - py) < 35 for px, py in positions):
                            positions.append((x, y))
                            num_under_table += 1
                            break
               

            # Draw the objects on the image
            for pos in positions:
                draw_object(draw, pos, color=random.choice(["red", "blue", "green", "yellow"]))

            # Save the image with numerical naming in the ./data folder
            image_filename = f"{file}.png"
            file += 1
            image_path = os.path.join(output_dir, image_filename)
            image.save(image_path)

            # Generate a random "gold output" for demonstration purposes
            gold_output = {
            "id": image_filename,
            "num_objects_over_table": num_over_table,
            "num_objects_under_table": num_under_table
            # "object_positions": positions
            }

            # Add the filename and gold output to the data dictionary
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

    print(f"Images saved in {output_dir} and data written to data.json.")


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
        help='List of n values',
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
    # print(num_object_list)
    # Create images with the specified number of objects
    # Directory to save images
    output_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    create_images(args.num_images, num_object_list , file)
