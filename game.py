import random
import time

# Game Introduction
def print_slow(str):
    for letter in str:
        print(letter, end='', flush=True)
        time.sleep(0.05)
    print()

def game_intro():
    print_slow("Welcome to the Adventure Game!")
    print_slow("In this game, you'll be traveling through different locations, solving puzzles, and facing challenges.")
    print_slow("Get ready for the adventure of a lifetime!")
    print()

# Main Game Functions
def encounter():
    print_slow("You come across a wild creature!")
    print_slow("Choose your action:")
    print_slow("1. Fight")
    print_slow("2. Flee")
    choice = input("Your choice (1 or 2): ")
    if choice == '1':
        fight()
    elif choice == '2':
        flee()
    else:
        print_slow("Invalid choice, try again.")
        encounter()

def fight():
    print_slow("You prepare to fight the creature!")
    outcome = random.choice(["win", "lose"])
    if outcome == "win":
        print_slow("You defeated the creature!")
    else:
        print_slow("The creature was too strong. You lost the battle!")

def flee():
    print_slow("You flee from the creature and escape safely.")

def solve_puzzle():
    print_slow("You reach a locked door with a puzzle on it.")
    print_slow("Solve the riddle to proceed.")
    print_slow("What has keys but can't open locks?")
    answer = input("Your answer: ")
    if answer.lower() == "piano":
        print_slow("Correct! The door opens.")
    else:
        print_slow("Incorrect! Try again.")
        solve_puzzle()

def adventure():
    game_intro()
    print_slow("Your journey begins in a mysterious forest...")
    time.sleep(2)
    print_slow("You walk deeper into the forest and suddenly...")
    encounter()
    print_slow("After the encounter, you continue your journey and find a locked door.")
    solve_puzzle()
    print_slow("You've completed your adventure! Congratulations!")

# Start the Game
if __name__ == "__main__":
    adventure()
