import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

# Define a custom color palette using hex codes or color names
custom_colors = ['black', 'gray', 'brown', 'maroon', 'red', 'coral', 'tan', 'orange', 'ivory', 'goldenrod', 'yellow', 'green', 'olive', 'turquoise', 'skyblue', 'blue', 'lavender', 'purple', 'pink', 'fuchsia']

# Create a ListedColormap from the custom colors
custom_cmap = ListedColormap(custom_colors)

# Create some dummy data to visualize the palette
data = np.arange(len(custom_colors)).reshape(1, -1)

# Display the custom color palette as a swatch
plt.figure(figsize=(6, 2))
plt.imshow(data, aspect='auto', cmap=custom_cmap)
plt.xticks(np.arange(len(custom_colors)), labels=custom_colors, rotation=90)
plt.yticks([])
plt.title("Color Palette Swatch for Reference")
plt.savefig("swatches.png", bbox_inches='tight')