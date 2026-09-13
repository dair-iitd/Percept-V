import networkx as nx
import matplotlib.pyplot as plt
import random
import argparse
import os
import json


def generate_graph(num_nodes, num_edges):
    # Create an empty graph
    G = nx.Graph()
    
    # Add nodes to the graph
    G.add_nodes_from(range(num_nodes))
    
    # Add edges to the graph
    possible_edges = [(i, j) for i in range(num_nodes) for j in range(i+1, num_nodes)]
    random_edges = random.sample(possible_edges, num_edges)
    G.add_edges_from(random_edges)
    
    return G

def draw_graph(G, idx):

    global file
    # Draw the graph
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G)  # Layout for visualization
    nx.draw(G, pos, with_labels=False, node_color='lightblue', edge_color='gray', node_size=2000, font_size=15)
    image_filename = f"{file}.png"
    file += 1
    image_path = os.path.join(output_dir, image_filename)
    plt.savefig(image_path)
    plt.close()

# Parameters: number of nodes and number of edges


# num_nodes = 10

# # Generate and draw the graph
# for i in range(1, 11):
#     num_edges = random.randint(10, 15)
#     G = generate_graph(num_nodes, num_edges)
#     draw_graph(G, idx=i)

if __name__ == '__main__':
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
        type = int,
        help='List of num of nodes',
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
    num_nodes = args.num_sizes
    num_images = args.num_images
    append = (file != 1)
    data = []
    
    for num_node in num_nodes:
        for i in range(num_images):
            if num_node == 1:
                num_edges = 0
            else:
                min_edge = min((num_node*(num_node-1))//2, (num_node+5))
                num_edges = random.randint(num_node-1, min_edge)
            G = generate_graph(num_node, num_edges)
            draw_graph(G, idx=i)
            data.append({
                "id": f"{file-1}.png",
                "num_nodes": num_node,
                "num_edges": num_edges
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
