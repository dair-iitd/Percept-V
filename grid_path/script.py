from PIL import Image, ImageDraw, ImageFont
import random
import argparse
import os
import json

def create_grid_image(n, m, image_size=800):
    global file, output_dir
    # Create a new image with white background
    img = Image.new('RGB', (image_size, image_size), 'white')
    draw = ImageDraw.Draw(img)

    image_list = []
    grid = []

    # Calculate cell size based on grid size
    cell_size = image_size // n
    border_color = 'black'
    shape_colors = ['red', 'green', 'blue', 'purple']
    # shape_colors = ['red']

    # Load a default font with a larger size for better visibility
    font_size = cell_size // 2
    font = ImageFont.truetype("arial.ttf", font_size)

    # Draw grid borders
    for i in range(n + 1):
        draw.line([(i * cell_size, 0), (i * cell_size, image_size)], fill=border_color, width=2)
        draw.line([(0, i * cell_size), (image_size, i * cell_size)], fill=border_color, width=2)

    # Add shapes inside each cell
    for i in range(n):
        row = []
        for j in range(n):
            shape_type = random.choice(['circle', 'square', 'triangle'])
            shape_color = random.choice(shape_colors)
            top_left = (j * cell_size + 5, i * cell_size + 5)
            bottom_right = ((j + 1) * cell_size - 5, (i + 1) * cell_size - 5)

            if shape_type == 'circle':
                draw.ellipse([top_left, bottom_right], fill=shape_color)
                row.append('circle')
            elif shape_type == 'square':
                draw.rectangle([top_left, bottom_right], fill=shape_color)
                row.append('square')
            elif shape_type == 'triangle':
                mid_x = (top_left[0] + bottom_right[0]) / 2
                draw.polygon([top_left, (bottom_right[0], top_left[1]), (mid_x, bottom_right[1])], fill=shape_color)
                row.append('triangle')
        grid.append(row)
    # print(grid)
    # Generate a random path of length m
    path = [(random.randint(0, n - 1), random.randint(0, n - 1))]
    while len(path) < m:
        last_x, last_y = path[-1]
        possible_moves = [(last_x + dx, last_y + dy) for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]]
        valid_moves = [(x, y) for x, y in possible_moves if 0 <= x < n and 0 <= y < n and (x, y) not in path]
        if valid_moves:
            path.append(random.choice(valid_moves))
        else:
            break  # No more moves possible

    # Draw the path with arrows and mark the start and end cells
    arrow_dict = {(1, 0): '→', (0, 1): '↓', (-1, 0): '←', (0, -1): '↑'}
    # print(path)
    for index in range(len(path) - 1):
        x1, y1 = path[index]
        x2, y2 = path[index + 1]
        start = (x1 * cell_size + cell_size // 2, y1 * cell_size + cell_size // 2)
        end = (x2 * cell_size + cell_size // 2, y2 * cell_size + cell_size // 2)
        draw.line([start, end], fill='black', width=4)
        # print(x1 , y1)
        image_list.append(grid[y1][x1])
        # Draw arrow in the middle of the line
        dx, dy = x2 - x1, y2 - y1
        if (dx, dy) in arrow_dict:
            arrow = arrow_dict[(dx, dy)]
            arrow_position = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2 - cell_size*0.045)
            # print(arrow_position , start , end)
            draw.text(arrow_position, arrow, fill='black', font=font, anchor="mm")
    
    # Label the start and end cells with larger and bolder text
    start_x, start_y = path[0]
    end_x, end_y = path[-1]
    draw.text((start_x * cell_size + cell_size // 2, start_y * cell_size + cell_size // 2), 'S', fill='black', font=font, anchor="mm")
    draw.text((end_x * cell_size + cell_size // 2, end_y * cell_size + cell_size // 2), 'E', fill='black', font=font, anchor="mm")

    image_list.append(grid[end_y][end_x])
    # Save the image
    # img.save('grid_image_with_path.png')
    image_filename = f"{file}.png"
    file += 1
    image_path = os.path.join(output_dir, image_filename)
    img.save(image_path)

    return image_list 
    

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
        help='List of n values',
        default=[5 , 3]
    )
    parser.add_argument(
        '--grid_size', 
        type=int, 
        help='Grid size', 
        default=6
    )
    parser.add_argument(
        '--file', 
        type=int, 
        help='Starting file number',
        default=1
    )
    args = parser.parse_args()
    file = args.file
    num_sizes = args.num_sizes
    append = (file != 1)
    data = []
    output_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for j in range(0, len(num_sizes)):
        for i in range(args.num_images):
            rows = args.grid_size
            path_size = int(num_sizes[j])
            image_list = create_grid_image(rows, path_size)
            # print(grid)
            data.append({
                'id': f"{file-1}.png",
                'rows': rows,
                'path_size': path_size,
                'gold_output': image_list
            })

    if append:
        with open(os.path.join(os.getcwd() , "data.json"), "r") as f:
            old_data = json.load(f)
            old_data.extend(data)
        with open(os.path.join(os.getcwd() , "data.json"), "w") as f:
            json.dump(old_data, f, indent=2)
    else:
        with open(os.path.join(os.getcwd() , "data.json"), "w") as f:
            json.dump(data, f, indent=2)