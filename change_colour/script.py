from PIL import Image, ImageDraw
import sys
import random
import os
import json
import argparse
import random


def create_images(num_images, num_objects_list , file):
    # Ensure that the directory exists
    # output_dir = "./data"
    output_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data = []
    image_width, image_height = 1500, 1000
    append = (file != 1)
    for num_objects in num_objects_list:
        max_obj = num_objects*2
        for img_index in range(num_images):
            # Create a blank white image
            image = Image.new("RGB", (image_width, image_height), "white")
            draw = ImageDraw.Draw(image)

            # List to hold positions of circles
            colour_dict = {1: "red", 2: "blue", 3: "green"}
            colours1 = []
            colours2 = []
            positions = []

            # Randomly select a radius for each circle
            radii = [random.randint(10, 30) for _ in range(max_obj)]

            # Generate non-overlapping positions for the circles
            while len(positions) < max_obj:
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
                    colours1.append(colour_dict[random.randint(1, 3)])
                    """colours2.append(colour_dict[random.randint(1, 3)])
                    if(colours1[-1] != colours2[-1]):
                        difference += 1"""
                    
            colours2 = colours1.copy()
            indices = random.sample(range(0, max_obj), num_objects)
            for index in indices:
                if(colours2[index] == 'red'):
                    colours2[index] = 'blue'
                elif(colours2[index] == 'blue'):
                    colours2[index] = 'green'
                else:
                    colours2[index] = 'red'

            # Draw the circles
            i=0
            for (x, y, radius) in positions:
                draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=colours1[i])
                i=i+1

            # Save the image with the filename `firsti.png`
            image_filename = f"first{file}.png"
            image_path = os.path.join(output_dir, image_filename)
            image.save(image_path)

            i=0
            for (x, y, radius) in positions:
                draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=colours2[i])
                i=i+1
            
            #Save the image with the filename `secondi.png`
            image_filename = f"second{file}.png"
            file += 1
            image_path = os.path.join(output_dir, image_filename)
            image.save(image_path)



            # Store the number of objects in the data dictionary
            # data[image_filename] = {
            #     "num_objects": num_objects
            # }
            gold_output = {
                "id": image_filename,
                "num_differences": num_objects
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