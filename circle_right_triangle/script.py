import matplotlib.pyplot as plt
import numpy as np
import random
import argparse
import os
import json

def create_shape_grid(rows, cols, circles_count, triangles_count):
    # Initialize the grid
    #right = random.choice([True, False])
    grid = np.empty((rows, cols), dtype=object)
    
    # Fill the grid with None
    for i in range(rows):
        for j in range(cols):
            grid[i, j] = None
    
    
    triangle_positions = []
    
    # Place triangles in the grid
    for _ in range(triangles_count):
        while True:
            row, col = random.randint(0, rows - 1), random.randint(0, cols - 1)
            if grid[row, col] is None:
                grid[row, col] = 'triangle'
                triangle_positions.append((row, col))
                # shapes_placed += 1
                break

    """shapes_placed = 0
    if right:
        #place atleast one circle to right of triangle and rest randomly
        placed_right = False
        for row, col in triangle_positions:
            if col < cols - 1 and grid[row, col + 1] is None:
                placed_right = True
                grid[row, col + 1] = 'circle'
                shapes_placed += 1
                break
        
        if not placed_right:
            right = False
            
        while shapes_placed < circles_count:
            row, col = random.randint(0, rows - 1), random.randint(0, cols - 1)
            if grid[row, col] is None:
                grid[row, col] = 'circle'
                shapes_placed += 1

    else:
        #no circle should be placed to the right of triangle
        while shapes_placed < circles_count:
            row, col = random.randint(0, rows - 1), random.randint(0, cols - 1)
            if col == 0 or grid[row, col - 1] != 'triangle':
                if grid[row, col] is None:
                    grid[row, col] = 'circle'
                    shapes_placed += 1"""
    
    positions = []
    for i in range(rows):
        for j in range(cols):
            positions.append((i, j))
    
    for pos in triangle_positions:
        positions.remove(pos)
    
    circle_positions = random.sample(positions, circles_count)
    for i, tup in enumerate(circle_positions):
        row, col = tup[0], tup[1]
        grid[row, col] = 'circle'

    right = False
    for i in range(rows):
        for j in range(cols-1):
            if grid[i, j] == 'triangle' and grid[i, j+1] == 'circle':
                right = True
                break

    return grid , right

def draw_grid(grid):
    global file, output_dir
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, grid.shape[1])
    ax.set_ylim(0, grid.shape[0])
    ax.set_xticks(np.arange(0, grid.shape[1] + 1))
    ax.set_yticks(np.arange(0, grid.shape[0] + 1))
    ax.grid(True)

    # Create cell outlines
    for i in range(grid.shape[0] + 1):
        ax.axhline(i, color='black', lw=1)
    for j in range(grid.shape[1] + 1):
        ax.axvline(j, color='black', lw=1)

    for (i, j), shape in np.ndenumerate(grid):
        if shape == 'circle':
            circle = plt.Circle((j + 0.5, grid.shape[0] - (i + 0.5)), 0.4, color='blue', ec='black')
            ax.add_artist(circle)
        elif shape == 'triangle':
            triangle = plt.Polygon([[j + 0.5, grid.shape[0] - (i + 0.1)], 
                                     [j + 0.1, grid.shape[0] - (i + 0.8)], 
                                     [j + 0.9, grid.shape[0] - (i + 0.8)]], 
                                    color='red', ec='black')
            ax.add_artist(triangle)

    ax.set_aspect('equal')
    plt.title('Grid of Circles and Triangles')
    
    #1 Save the image if the output directory exists
    image_filename = f"{file}.png"
    file += 1
    image_path = os.path.join(output_dir, image_filename)
    
    # Uncomment below if you want to save the figure
    plt.savefig(image_path)
    plt.close()
    
    # plt.show()

# # Input for grid dimensions, number of circles, and triangles
# num_rows = 5  # Number of rows
# num_cols = 5 # Number of columns
# num_circles = 3 # Number of circles
# num_triangles = 3  # Number of triangles

# grid = create_shape_grid(num_rows, num_cols, num_circles, num_triangles)
# draw_grid(grid)

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
        help='List of n values (grid size , number of shapes) to generate', 
        default=[3 , 1]
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
    data = []
    append = (file != 1)
    output_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for j in range(0, len(num_sizes)):
        for i in range(args.num_images):
            rows, cols = args.grid_size, args.grid_size
            circles = int(num_sizes[j])
            triangles = min(int(num_sizes[j]), args.grid_size**2 - int(num_sizes[j]))
            grid,right = create_shape_grid(rows, cols, circles, triangles)
            # print(grid)
            data.append({
                'id': f"{file}.png",
                'rows': rows,
                'cols': cols,
                'circles': circles,
                'triangles': triangles,
                'right': right
            })
            draw_grid(grid)
    if append:
        with open(os.path.join(os.getcwd() , "data.json"), "r") as f:
            old_data = json.load(f)
            old_data.extend(data)
        with open(os.path.join(os.getcwd() , "data.json"), "w") as f:
            json.dump(old_data, f, indent=2)
    else:
        with open(os.path.join(os.getcwd() , "data.json"), "w") as f:
            json.dump(data, f, indent=2)