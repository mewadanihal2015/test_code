import keyboard
import time

# Define your game actions
def move_forward():
    print("Moving forward")

def move_backward():
    print("Moving backward")

def move_left():
    print("Moving left")

def move_right():
    print("Moving right")

def jump():
    print("Jump!")

def quit_game():
    print("Quitting game...")
    global running
    running = False

# Create a mapping between keys and actions
key_bindings = {
    'w': move_forward,
    's': move_backward,
    'a': move_left,
    'd': move_right,
    'space': jump,
    'esc': quit_game
}

# Main loop
print("Game controls ready! (WASD to move, SPACE to jump, ESC to quit)")

running = True
while running:
    for key, action in key_bindings.items():
        if keyboard.is_pressed(key):
            action()
            time.sleep(0.2)  # Prevents action spamming
