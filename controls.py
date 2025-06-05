import pygame
import sys

# Initialize pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Game Control Mapping")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define control mappings
controls = {
    "move_left": pygame.K_a,
    "move_right": pygame.K_d,
    "jump": pygame.K_SPACE,
    "shoot": pygame.K_RETURN,
    "quit": pygame.K_ESCAPE
}

# Game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle key presses
        if event.type == pygame.KEYDOWN:
            if event.key == controls["move_left"]:
                print("Move left")
            elif event.key == controls["move_right"]:
                print("Move right")
            elif event.key == controls["jump"]:
                print("Jump")
            elif event.key == controls["shoot"]:
                print("Shoot")
            elif event.key == controls["quit"]:
                running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
