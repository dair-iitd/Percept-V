from PIL import Image, ImageDraw
import random
import os
import argparse
import json
# Global counter to ensure unique numbering across the entire maze
current_path_number = 1
end_x, end_y = 1, 1
path_length = 3

def create_grid(n, m):
    grid = [['#' for _ in range(m)] for _ in range(n)]
    return grid

def carve_path(grid, x, y):
    global current_path_number
    global end_x, end_y
    global path_length
    grid[x][y] = str(current_path_number)
    current_path_number += 1
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    random.shuffle(directions)

    for dx, dy in directions:
        nx, ny = x + dx * 2, y + dy * 2
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == '#':
            grid[x + dx][y + dy] = str(current_path_number)
            if current_path_number == path_length:
                end_x, end_y = x+dx, y+dy
            current_path_number += 1
            carve_path(grid, nx, ny)

def find_solution(grid, start_pos, end_pos):
    # BFS to find the optimal path
    from collections import deque
    
    n, m = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = deque([(start_pos, [grid[start_pos[0]][start_pos[1]]])])
    visited = set([start_pos])

    while queue:
        (x, y), path = queue.popleft()
        
        if (x, y) == end_pos:
            return path
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and (nx, ny) not in visited and grid[nx][ny] != '#':
                queue.append(((nx, ny), path + [grid[nx][ny]]))
                visited.add((nx, ny))
    
    return []

def generate_maze(n, m, path):
    global current_path_number
    global path_length
    current_path_number = 1  # Reset global counter for new maze
    path_length = path

    grid = create_grid(n, m)
    start_x, start_y = random.choice(range(1, n, 2)), random.choice(range(1, m, 2))
    carve_path(grid, start_x, start_y)
    
    # Set the end position at the farthest point from the start
    #end_x, end_y = random.choice(range(1, n, 2)), random.choice(range(1, m, 2))
    
    # Ensure start and end are not the same
    """while (end_x, end_y) == (start_x, start_y):
        end_x, end_y = random.choice(range(1, n, 2)), random.choice(range(1, m, 2))"""
    
    global end_x, end_y
    if end_x == 1 and end_y == 1:
        for x in range(n):
            for y in range(m):
                if grid[x][y] == str(path_length):
                    end_x, end_y = x, y
                    break
    grid[start_x][start_y] = "S"  # Label the start
    grid[end_x][end_y] = "E"  # Label the end
    
    solution = find_solution(grid, (start_x, start_y), (end_x, end_y))
    end_x, end_y = 1, 1
    return grid, (start_x, start_y), (end_x, end_y), solution

def maze_to_image(grid, cell_size=40):
    n, m = len(grid), len(grid[0])
    img = Image.new("RGB", (m * cell_size, n * cell_size), color="white")
    draw = ImageDraw.Draw(img)

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            top_left = (j * cell_size, i * cell_size)
            bottom_right = ((j + 1) * cell_size, (i + 1) * cell_size)
            draw.rectangle([top_left, bottom_right], outline="black", width=1)  # Draw cell borders
            if cell == '#':
                draw.rectangle([top_left, bottom_right], fill="black")
            elif cell == 'S':  # Start cell
                draw.rectangle([top_left, bottom_right], fill="white" , outline="black", width=1)
                draw.text((top_left[0] + cell_size//4, top_left[1] + cell_size//4), "S", fill="black")
                
            elif cell == 'E':  # End cell
                draw.rectangle([top_left, bottom_right], fill="white" , outline="black", width=1)
                draw.text((top_left[0] + cell_size//4, top_left[1] + cell_size//4), "E", fill="black")
            else:
                draw.rectangle([top_left, bottom_right], fill="white" , outline="black", width=1)
                draw.text((top_left[0] + cell_size//4, top_left[1] + cell_size//4), cell, fill="blue")
    
    return img

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
        type=int,
        help='List of n values (num rows , num columns) to generate', 
        default=[5 , 5]
    )
    parser.add_argument(
        '--file', 
        type=int, 
        help='Starting file number',
        default=1
    )
    args = parser.parse_args()

    file = args.file
    data = []
    append = (file != 1)
    num_images = args.num_images
    num_size = args.num_sizes
    # num_images = int(sys.argv[1])
    # num_size = sys.argv[2:]
    # num_size = [int(num_objects) for num_objects in num_size]
    # n, m = 11, 11  # Dimensions of the maze (should be odd numbers)
    for i in range(0 , len(num_size)):
        n = 11
        m = 11
        for _ in range(num_images):
            maze, start_pos, end_pos, solution = generate_maze(n, m, num_size[i])
            # solution = [int(cell) for cell in solution]
            img = maze_to_image(maze)
            # img.show()
            gold_output = {
                "id": f"{file}.png",
                "path": solution,
                "Rows": n,
                "Columns": m
            }
            file += 1
            data.append(gold_output)
            img.save(os.path.join(output_dir, gold_output["id"]))
    
    if append:
        with open(os.path.join(os.getcwd() , "data.json"), "r") as f:
            old_data = json.load(f)
            old_data.extend(data)
        with open(os.path.join(os.getcwd() , "data.json"), "w") as f:
            json.dump(old_data, f, indent=2)
    else:
        with open(os.path.join(os.getcwd() , "data.json"), "w") as f:
            json.dump(data, f, indent=2)
    # maze, start_pos, end_pos, solution = generate_maze(n, m)
    # print("Optimal Solution Path (cell numbers):", solution)
    # img = maze_to_image(maze)
    # img.show()
    