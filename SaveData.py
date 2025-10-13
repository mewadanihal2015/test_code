import json

def save_data_json(filename, data):
    with open(filename, 'w') as file:  # 'w' overwrites the file
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")

def load_data_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

# Example usage
game_data = {
    "player": "Alice",
    "score": 1500,
    "level": 4,
    "inventory": ["sword", "shield", "potion"]
}

save_data_json("savefile.json", game_data)

# Load it back
loaded_data = load_data_json("savefile.json")
print("Loaded Data:", loaded_data)
