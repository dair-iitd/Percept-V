from PIL import Image, ImageDraw, ImageFont
import random
import argparse
import os
import json

def create_labeled_grid(n, m, cell_size=100, margin=40):
    """
    Create and save an image with a labeled grid.
    
    Args:
        rows (int): Number of rows in the grid
        cols (int): Number of columns in the grid
        cell_size (int): Size of each cell in pixels
        margin (int): Margin around the grid for labels
        filename (str): Name of the output file
    """
    global file, output_dir

    rows = cols = n

    # Calculate total size including margins for labels
    width = cols * cell_size + 2 * margin
    height = rows * cell_size + 2 * margin
    
    # Create a new white image
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Try to use Arial font, fall back to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", size=20)
    except IOError:
        font = ImageFont.load_default()
    
    # Draw vertical lines and column labels
    for i in range(cols + 1):
        x = margin + i * cell_size
        # Draw vertical line
        draw.line([(x, margin), (x, height - margin)], fill='black', width=2)
        # Draw column label (skip last number)
        if i < cols:
            label = str(i + 1)
            # Get text size for centering
            text_bbox = draw.textbbox((0, 0), label, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            draw.text((x + (cell_size - text_width) // 2, margin // 2), 
                     label, fill='black', font=font)
    
    # Draw horizontal lines and row labels
    for i in range(rows + 1):
        y = margin + i * cell_size
        # Draw horizontal line
        draw.line([(margin, y), (width - margin, y)], fill='black', width=2)
        # Draw row label (skip last number)
        if i < rows:
            # Changed from letters to numbers
            label = str(i + 1)
            text_bbox = draw.textbbox((0, 0), label, font=font)
            text_height = text_bbox[3] - text_bbox[1]
            draw.text((margin // 2, y + (cell_size - text_height) // 2), 
                     label, fill='black', font=font)
            
    shape_colors = ['red', 'blue', 'purple' , 'yellow']
    shape_types = ['circle']

    coord_list = []
    
    # for random m cells draw a green circle in them
    k = 0

    while k < m:
        i = random.randint(0, rows - 1)
        j = random.randint(0, cols - 1)
        if (i+1, j+1) in coord_list:
            # k -= 1
            continue
        # print(k , i, j)
        top_left = (margin + j * cell_size + 5, margin + i * cell_size + 5)
        bottom_right = (margin + (j + 1) * cell_size - 5, margin + (i + 1) * cell_size - 5)
        draw.ellipse([top_left, bottom_right], fill='green')
        coord_list.append((i+1, j+1))
        k += 1
    
    for i in range(rows):
        for j in range(cols):
            if (i+1, j+1) not in coord_list:
                shape_type = random.choice(shape_types)
                if shape_type != 'circle':
                    shape_color = random.choice(shape_colors + ['green'])
                else:
                    shape_color = random.choice(shape_colors)
                top_left = (margin + j * cell_size + 5, margin + i * cell_size + 5)
                bottom_right = (margin + (j + 1) * cell_size - 5, margin + (i + 1) * cell_size - 5)
                if shape_type == 'circle':
                    draw.ellipse([top_left, bottom_right], fill=shape_color)
                elif shape_type == 'square':
                    draw.rectangle([top_left, bottom_right], fill=shape_color)
                elif shape_type == 'triangle':
                    mid_x = (top_left[0] + bottom_right[0]) / 2
                    draw.polygon([top_left, (bottom_right[0], top_left[1]), (mid_x, bottom_right[1])], fill=shape_color)


    image_filename = f"{file}.png"
    file += 1
    image_path = os.path.join(output_dir, image_filename)
    image.save(image_path)

    return coord_list

# Example usage
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
            n_circles = int(num_sizes[j])
            coord_list = create_labeled_grid(rows, n_circles)
            # print(grid)
            data.append({
                'id': f"{file-1}.png",
                'rows': rows,
                'n_circles': n_circles,
                'gold_output': coord_list
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