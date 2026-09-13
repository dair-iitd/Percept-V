import numpy as np
import matplotlib.pyplot as plt
import random
import os
import json
import argparse


def create_grid_with_crosses(n, k , output_dir):
    # Create a figure and axis
    global file
    
    fig, ax = plt.subplots()

    # Set the limits of the grid
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)

    # Disable axis labels and ticks
    ax.set_xticks(np.arange(0, n+1, 1))
    ax.set_yticks(np.arange(0, n+1, 1))
    ax.grid(True)
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

    # Randomly select k unique cells for crosses
    if (k < n*n):
        crosses = set()
        while len(crosses) < k:
            cross_position = (random.randint(0, n-1), random.randint(0, n-1))
            crosses.add(cross_position)

        # Store cross positions in a list
        cross_list = list(crosses)
    else:
        cross_list = []
        crosses = set()
        for i in range(n):
            for j in range(n):
                cross_list.append((i,j))
                crosses.add((i,j))
        

    # Label the cells (i,j) that don't have crosses
    for i in range(n):
        for j in range(n):
            if (i, j) not in crosses:
                label = f"({i},{j})"
                ax.text(j + 0.5, n - i - 0.5, label, va='center', ha='center', fontsize=8, color='blue')
            else:
                ax.text(j + 0.5, n - i - 0.5, 'X', va='center', ha='center', fontsize=25, color='black')

    # Draw grid lines
    ax.set_xticks(np.arange(0, n+1, 1), minor=False)
    ax.set_yticks(np.arange(0, n+1, 1), minor=False)
    plt.grid(True)

    # Show the plot
    plt.gca().set_aspect('equal', adjustable='box')
    # plt.show()
    image_filename = f"{file}.png"
    file += 1
    image_path = os.path.join(output_dir, image_filename)
    plt.savefig(image_path)
    plt.close()

    return cross_list


def is_safe_from_cross(crosses, i, j, n):
    """Checks if all non-diagonal adjacent cells of (i, j) do not contain crosses."""
    # Define directions for non-diagonal moves (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1) , (0,0)]
    
    for di, dj in directions:
        ni, nj = i + di, j + dj
        # Check if the adjacent cell is within bounds and contains a cross
        if 0 <= ni < n and 0 <= nj < n:
            if (ni, nj) in crosses:
                return False
    return True

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate data for cross and knots")
    parser.add_argument(
        '--num_images', 
        type=int, 
        help='Number of images to generate',
        default=1
    )
    parser.add_argument(
        '--num_sizes', 
        nargs='*', 
        help='List of n values (grid size , number of crosses) to generate',
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
        help='Output directory',
        default=1
    )
    args = parser.parse_args()
    num_images = args.num_images
    num_sizes = args.num_sizes
    file = args.file    
    append = (file != 1)
    # num_images = int(sys.argv[1])
    # num_sizes = sys.argv[2:]
    # # print(num_images)
    # file = 1
    data  = []
    output_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for j in range(0, len(num_sizes)):
        for i in range(num_images):
            n = args.grid_size
            crosses = int(num_sizes[j])
            # print(n,k)
            cross_positions = create_grid_with_crosses(args.grid_size, crosses , output_dir)

            safe_cells = []
            for k in range(n):
                for l in range(n):
                    if is_safe_from_cross(set(cross_positions), k, l, n):
                        safe_cells.append((k, l))

            data.append({
                "id" : f"{file-1}.png",
                "n" : args.grid_size,    
                "crosses" : crosses,
                "cross_positions" : cross_positions,
                "gold_output" : safe_cells
            })
            # Print the list of cross positions
            # print("Cross positions:", cross_positions)
    if append:
        with open(os.path.join(os.getcwd() , "data.json"), "r") as f:
            old_data = json.load(f)
            old_data.extend(data)
        with open(os.path.join(os.getcwd() , "data.json"), "w") as f:
            json.dump(old_data, f, indent=2)
    else:
        with open(os.path.join(os.getcwd() , "data.json"), "w") as f:
            json.dump(data, f, indent=2)


