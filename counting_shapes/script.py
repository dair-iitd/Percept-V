from PIL import Image, ImageDraw
import random
import os
import json
import argparse

num_circle = 0 
num_triangle = 0
num_square = 0

def random_shape(draw, shape_type, x, y, size):
    """
    Draw a random shape on the provided image.
    """
    global num_circle, num_square, num_triangle, num_star
    if shape_type == "circle":
        draw.ellipse([x - size, y - size, x + size, y + size], fill="black")
        num_circle +=1
    elif shape_type == "square":
        draw.rectangle([x - size, y - size, x + size, y + size], fill="black")
        num_square +=1
    elif shape_type == "triangle":
        points = [
            (x, y - size),  # Top
            (x - size, y + size),  # Bottom left
            (x + size, y + size),  # Bottom right
        ]
        draw.polygon(points, fill="black")
        num_triangle +=1

def create_images(num_images, num_objects_list , file):
    # Ensure the output directory exists
    global num_circle, num_square, num_triangle, num_star
    output_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data = []
    image_width, image_height = 500, 300
    append = (file != 1)
    for num_objects in num_objects_list:
        for img_index in range(num_images):
            # Create a blank white image
            image = Image.new("RGB", (image_width, image_height), "white")
            draw = ImageDraw.Draw(image)

            # List to hold positions and sizes of shapes
            shapes = []
            num_circle =0 
            num_triangle = 0
            num_star = 0
            num_square = 0


            # Possible shape types
            shape_types = ["circle", "square", "triangle"]

            while len(shapes) < num_objects:
                shape_type = random.choice(shape_types)
                size = random.randint(10, 20)
                x = random.randint(size+50, image_width - size - 50)
                y = random.randint(size + 50, image_height - size - 50)

                # Check if the new shape overlaps or touches any existing shapes
                overlap = False
                for (sx, sy, ssize,_) in shapes:
                    distance = ((sx - x) ** 2 + (sy - y) ** 2) ** 0.5
                    if distance < (ssize + size)*1.5:
                        overlap = True
                        break

                if not overlap:
                    shapes.append((x, y, size, shape_type))
            # print(shapes)
            # Draw the shapes
            for (x, y, size, shape_type) in shapes:
                random_shape(draw, shape_type, x, y, size)

            # Save the image with the filename `i.png`
            image_filename = f"{file}.png"
            file += 1
            image_path = os.path.join(output_dir, image_filename)
            image.save(image_path)

            # Store the number of objects in the data dictionary
            gold_output = {
                "id": image_filename,
                "circles" : num_circle,
                "squares" : num_square,
                "triangles" : num_triangle
            }
            data.append(gold_output)

    # Save the data to a JSON file
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
        help='List of num shapes',
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
    # print(num_object_list)
    # Create images with the specified number of objects
    create_images(args.num_images, num_object_list , file)
