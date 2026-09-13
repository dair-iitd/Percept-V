from PIL import Image, ImageDraw
import random
import os
import json
import argparse

def create_images(num_images, num_objects_list , file):
    # Ensure that the directory exists
    # output_dir = "./data"
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

            # List to hold positions of circles
            positions = []

            # Randomly select a radius for each circle
            radii = [random.randint(10, 30) for _ in range(num_objects)]

            # Generate non-overlapping positions for the circles
            while len(positions) < num_objects:
                x = random.randint(max(radius for radius in radii), image_width - max(radius for radius in radii))
                y = random.randint(max(radius for radius in radii), image_height - max(radius for radius in radii))

                # Check if the new circle overlaps or touches any existing circles
                overlap = False
                for (px, py, r) in positions:
                    distance = ((px - x) ** 2 + (py - y) ** 2) ** 0.5
                    if distance < r + max(radii):
                        overlap = True
                        break

                if not overlap:
                    radius = radii[len(positions)]
                    positions.append((x, y, radius))

            # Draw the circles
            for (x, y, radius) in positions:
                draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill="black")

            # Save the image with the filename `i.png`
            image_filename = f"{file}.png"
            file += 1
            image_path = os.path.join(output_dir, image_filename)
            image.save(image_path)

            # Store the number of objects in the data dictionary
            # data[image_filename] = {
            #     "num_objects": num_objects
            # }
            gold_output = {
                "id": image_filename,
                "num_objects": num_objects
            }
            data.append(gold_output)

            # print(f"Image saved at: {image_path}")

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
    create_images(args.num_images, num_object_list , file)
