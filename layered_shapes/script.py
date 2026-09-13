from PIL import Image, ImageDraw
import random
import os
import json
import argparse
import math



def generate_depth_images(num_images , num_object_list , file , image_size=(1800, 1800)):
    output_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data = []
    append = (file != 1)

    for n in num_object_list:
        for _ in range(num_images):  
            canvas = Image.new("RGB", image_size, (255, 255, 255))
            draw = ImageDraw.Draw(canvas)
            def color_distance(c1, c2):
                return sum((a - b) ** 2 for a, b in zip(c1, c2))
            
            def generate_distinct_colors(n, min_diff=500):
                colors = []
                while len(colors) < n:
                    new_color = (random.randint(50, 205), random.randint(50, 205), random.randint(50, 205))
                    if all(color_distance(new_color, c) > min_diff for c in colors):
                        colors.append(new_color)
                return colors
            
            colors = generate_distinct_colors(n)
            # colors = [(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)) for _ in range(n)]
            #shapes = [ 'triangle' , 'square' , 'pentagon', 'hexagon']
            shapes = ['diamond', 'hexagon', 'octagon']
            
            center_x, center_y = image_size[0] // 2, image_size[1] // 2  # Keep all shapes centered
            
            def draw_polygon(sides, radius, center, color):
                angle = 360 / sides
                points = [
                    (
                        center[0] + radius * math.cos(math.radians(i * angle)),
                        center[1] + radius * math.sin(math.radians(i * angle))
                    )
                    for i in range(sides)
                ]
                draw.polygon(points, outline='black', fill=color)

            order = []
            prev_size = 800
            for i in reversed(range(n)):  # Draw from back to front

                size = prev_size
                shape_type = random.choice(shapes)
                order.append(shape_type)

                if shape_type == 'diamond':
                    draw_polygon(4 , size, (center_x, center_y), colors[i])
                    prev_size = size*math.cos(math.radians(45))
                elif shape_type == 'circle':
                    draw_polygon(360, (size-((i/n)*200)), (center_x, center_y), colors[i])
                    prev_size = size
                elif shape_type == 'octagon':
                    draw_polygon(8, size, (center_x, center_y), colors[i])
                    prev_size = size*math.cos(math.radians(22.5))
                elif shape_type == 'hexagon':
                    draw_polygon(6, size, (center_x, center_y), colors[i])
                    prev_size = size*math.cos(math.radians(30))
                
                #prev_size -= (200/n)


            image_filename = f"{file}.png"
            file += 1
            image_path = os.path.join(output_dir, image_filename)
            canvas.save(image_path)

            reversed_order = order[::-1]

            gold_output = {
                "id": image_filename,
                "num_layers" : n,
                "order": reversed_order,    
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
