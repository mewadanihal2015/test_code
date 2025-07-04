import random
import json

# Define character attributes
GENDERS = ["Male", "Female", "Non-binary"]
RACES = ["Human", "Elf", "Dwarf", "Orc", "Halfling", "Tiefling"]
CLASSES = ["Warrior", "Mage", "Rogue", "Cleric", "Ranger", "Bard"]
HAIR_COLORS = ["Black", "Brown", "Blonde", "Red", "White", "Blue", "Green"]
EYE_COLORS = ["Brown", "Blue", "Green", "Hazel", "Gray", "Amber"]
CLOTHING_STYLES = ["Robes", "Leather Armor", "Plate Armor", "Tunic", "Cloak"]
PERSONALITY_TRAITS = ["Brave", "Cunning", "Honorable", "Greedy", "Loyal", "Reckless"]

# Define stats ranges
STAT_NAMES = ["Strength", "Agility", "Intelligence", "Charisma", "Endurance", "Luck"]
STAT_RANGE = (1, 10)  # 1 to 10 scale

def random_stats():
    """Generates random stats for a character."""
    return {stat: random.randint(*STAT_RANGE) for stat in STAT_NAMES}

def random_backstory(race, cls):
    """Generates a simple random backstory snippet."""
    templates = [
        f"Raised as a {race} in the wilderness, this {cls.lower()} learned to survive against all odds.",
        f"Once a noble {race}, they abandoned their title to become a wandering {cls.lower()}.",
        f"A {cls.lower()} with a mysterious past, rumored to be connected to an ancient prophecy.",
        f"As a {race} child, they were trained in secret arts to become a formidable {cls.lower()}."
    ]
    return random.choice(templates)

def generate_character(name=None):
    """Generates a random character."""
    character = {
        "Name": name if name else f"NPC_{random.randint(1000, 9999)}",
        "Gender": random.choice(GENDERS),
        "Race": random.choice(RACES),
        "Class": random.choice(CLASSES),
        "Hair Color": random.choice(HAIR_COLORS),
        "Eye Color": random.choice(EYE_COLORS),
        "Clothing": random.choice(CLOTHING_STYLES),
        "Personality": random.sample(PERSONALITY_TRAITS, 2),
        "Stats": random_stats(),
        "Backstory": None  # Placeholder to add below
    }
    character["Backstory"] = random_backstory(character["Race"], character["Class"])
    return character

def save_character(character, filename="character.json"):
    """Saves the character data to a JSON file."""
    with open(filename, "w") as f:
        json.dump(character, f, indent=4)
    print(f"Character saved to {filename}")

def print_character(character):
    """Prints the character details in a readable format."""
    print("=== Character Profile ===")
    for key, value in character.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for stat, val in value.items():
                print(f"  {stat}: {val}")
        elif isinstance(value, list):
            print(f"{key}: {', '.join(value)}")
        else:
            print(f"{key}: {value}")

# Example usage
if __name__ == "__main__":
    new_character = generate_character()
    print_character(new_character)
    save_character(new_character, "generated_character.json")
