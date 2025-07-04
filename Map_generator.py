import random
from PIL import Image

# Define terrain types and their colors
TERRAINS = {
    "water": (28, 107, 160),     # blue
    "grass": (34, 139, 34),      # green
    "mountain": (139, 137, 137), # gray
    "forest": (0, 100, 0),       # dark green
    "sand": (237, 201, 175),     # sand color
}

# Terrain generation weights (adjust to control terrain frequency)
TERRAIN_WEIGHTS = {
    "water": 0.2,
    "grass": 0.4,
    "mountain": 0.1,
    "forest": 0.2,
    "sand": 0.1,
}

def generate_random_map(width, height):
    """Generates a random map as a 2D grid of terrain types."""
    terrain_list = list(TERRAINS.keys())
    weights = [TERRAIN_WEIGHTS[t] for t in terrain_list]
    
    grid = [
        [random.choices(terrain_list, weights=weights)[0] for _ in range(width)]
        for _ in range(height)
    ]
    return grid

def print_map(grid):
    """Prints the map to the console using symbols."""
    terrain_symbols = {
        "water": "~",
        "grass": ".",
        "mountain": "^",
        "forest": "♣",
        "sand": "*",
    }
    for row in grid:
        print(" ".join(terrain_symbols[cell] for cell in row))

def save_map_image(grid, filename="random_map.png", cell_size=10):
    """Saves the map as an image."""
    height = len(grid)
    width = len(grid[0])
    img = Image.new("RGB", (width * cell_size, height * cell_size))
    pixels = img.load()

    for y, row in enumerate(grid):
        for x, terrain in enumerate(row):
            color = TERRAINS[terrain]
            for dy in range(cell_size):
                for dx in range(cell_size):
                    pixels[x * cell_size + dx, y * cell_size + dy] = color

    img.save(filename)
    print(f"Map saved to {filename}")

# Example usage
if __name__ == "__main__":
    map_width = 50
    map_height = 30

    random_map = generate_random_map(map_width, map_height)
    print_map(random_map)
    save_map_image(random_map, "generated_map.png")
