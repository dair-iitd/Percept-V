from PIL import Image, ImageDraw, ImageFont
import random
import os
import json
import argparse

def generate_parallel_lines(n=5, image_size=(1000, 1000) , min_size_diff=20):

    global file

    canvas = Image.new("RGB", image_size, (255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    
    line_spacing = image_size[0] // (n + 1)
    base_y = image_size[1] - 10  # Common base for all lines
    
    min_length = image_size[1] // 4
    max_length = image_size[1] - 40
    
    lengths = []
    # prev_length = random.randint(min_length, max_length)
    # lengths.append(prev_length)
    
    for _ in range(0, n):
        new_length = random.randint(min_length, max_length)
        # for prev_length in lengths:
        #     while abs(new_length - prev_length) < min_size_diff:
        #         new_length = random.randint(min_length, max_length)
        # lengths.append(new_length)
        # prev_length = new_length
        #Check all length in lengths for minimumm size difference   
        while any([abs(new_length - prev_length) < min_size_diff for prev_length in lengths]):
            new_length = random.randint(min_length, max_length)
        lengths.append(new_length)
        
    
    for i in range(n):
        x = (i + 1) * line_spacing
        line_length = lengths[i]
        start_y = base_y - line_length
        end_y = base_y
        color = (random.randint(50, 205), random.randint(50, 205), random.randint(50, 205))
        
        draw.line([(x, start_y), (x, end_y)], fill=color, width=3)
        font = ImageFont.truetype('ARIAL.ttf', 30)
        draw.text((x - 10, start_y - 30), f"{i+1}", fill=(0, 0, 0), font=font)

    to_sort = [{"label": i+1, "length": lengths[i]} for i in range(n)]
    sorted_lines = sorted(to_sort, key=lambda x: x['length'])
    gold_output = sorted_lines

    image_filename = f"{file}.png"
    image_path = os.path.join(output_dir, image_filename)
    canvas.save(image_path)

    return gold_output


if __name__ == "__main__":
    output_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
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
        help='List of n values',
        type=int,
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
    num_images = args.num_images
    append = (file != 1)
    data = []
    for num_circles in num_object_list:
        for _ in range(num_images):
            output = generate_parallel_lines(num_circles)
            gold_output = [circle['label'] for circle in output]
            gold_output = {
                "id": f'{file}.png',
                "Gold_output": gold_output,
                "Lines" : num_circles
            }
            file += 1
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
