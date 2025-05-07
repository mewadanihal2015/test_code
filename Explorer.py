import random
import time

# Function to print text slowly for effect
def print_slow(str):
    for letter in str:
        print(letter, end='', flush=True)
        time.sleep(0.05)
    print()

# Game Introduction
def game_intro():
    print_slow("Welcome to Space Explorer!")
    print_slow("In this game, you will be exploring outer space, encountering alien life forms, and managing your spaceship.")
    print_slow("Make wise decisions, as the fate of your crew depends on you!")
    print()

# Main Game Functions
def space_encounter():
    print_slow("You've encountered an unknown alien ship!")
    print_slow("Choose your action:")
    print_slow("1. Communicate")
    print_slow("2. Attack")
    print_slow("3. Flee")
    choice = input("Your choice (1, 2, or 3): ")
    if choice == '1':
        communicate()
    elif choice == '2':
        attack()
    elif choice == '3':
        flee()
    else:
        print_slow("Invalid choice, try again.")
        space_encounter()

def communicate():
    print_slow("You open communications with the alien ship...")
    outcome = random.choice(["friendly", "hostile"])
    if outcome == "friendly":
        print_slow("The aliens are friendly and share valuable resources with you!")
    else:
        print_slow("The aliens turn hostile and attack your ship!")
        attack()

def attack():
    print_slow("You decide to attack the alien ship!")
    outcome = random.choice(["win", "lose"])
    if outcome == "win":
        print_slow("You successfully destroy the alien ship and continue your journey.")
    else:
        print_slow("Your attack fails, and the alien ship damages your ship. You need to repair it!")
        repair_ship()

def flee():
    print_slow("You decide to flee from the alien ship.")
    print_slow("After a tense chase, you manage to escape safely, but your resources are low.")

def repair_ship():
    print_slow("You need to repair your spaceship. Do you have enough resources?")
    resources = random.randint(1, 3)
    print_slow(f"You have {resources} repair resources available.")
    if resources >= 2:
        print_slow("You successfully repair the ship and continue your journey.")
    else:
        print_slow("You don't have enough resources to repair the ship. Your journey ends here.")

def explore_planet():
    print_slow("You land on a mysterious planet.")
    print_slow("Would you like to:")
    print_slow("1. Explore the planet's surface")
    print_slow("2. Collect resources")
    print_slow("3. Leave the planet")
    choice = input("Your choice (1, 2, or 3): ")
    if choice == '1':
        print_slow("You find strange alien ruins. But beware, they might be dangerous!")
    elif choice == '2':
        print_slow("You collect valuable minerals from the planet's surface.")
    elif choice == '3':
        print_slow("You decide to leave the planet and continue your journey.")
    else:
        print_slow("Invalid choice, try again.")
        explore_planet()

def space_exploration():
    game_intro()
    print_slow("Your adventure begins aboard the starship Voyager, heading into uncharted space...")
    time.sleep(2)
    print_slow("You encounter a mysterious alien ship on the horizon...")
    space_encounter()
    print_slow("You continue your exploration and land on a strange planet.")
    explore_planet()
    print_slow("Your journey continues through the vastness of space. Who knows what you'll discover next?")
    print_slow("Thanks for playing Space Explorer!")

# Start the Game
if __name__ == "__main__":
    space_exploration()
