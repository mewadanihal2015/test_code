import tkinter as tk
import random

# Window settings
WIDTH = 800
HEIGHT = 500

# Ball settings
BALL_RADIUS = 15
x = 100
y = 100
dx = 5
dy = 4

# Trigger zone (vertical strip)
ZONE_X1 = 350
ZONE_X2 = 450

# Name to draw
NAME = "OpenAI"

# Prevent repeated drawing while ball remains in zone
inside_zone = False

root = tk.Tk()
root.title("Bouncing Ball Name Drawer")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

# Draw trigger zone
canvas.create_rectangle(
    ZONE_X1, 0, ZONE_X2, HEIGHT,
    fill="#e6f3ff",
    outline="blue"
)

# Create ball
ball = canvas.create_oval(
    x - BALL_RADIUS,
    y - BALL_RADIUS,
    x + BALL_RADIUS,
    y + BALL_RADIUS,
    fill="red"
)


def draw_name():
    """Draw the name at a random location."""
    text_x = random.randint(50, WIDTH - 50)
    text_y = random.randint(30, HEIGHT - 30)

    canvas.create_text(
        text_x,
        text_y,
        text=NAME,
        font=("Arial", 18, "bold"),
        fill=random.choice([
            "blue", "green", "purple",
            "orange", "black"
        ])
    )


def animate():
    global x, y, dx, dy, inside_zone

    # Update position
    x += dx
    y += dy

    # Bounce off walls
    if x - BALL_RADIUS <= 0 or x + BALL_RADIUS >= WIDTH:
        dx *= -1

    if y - BALL_RADIUS <= 0 or y + BALL_RADIUS >= HEIGHT:
        dy *= -1

    # Move ball
    canvas.coords(
        ball,
        x - BALL_RADIUS,
        y - BALL_RADIUS,
        x + BALL_RADIUS,
        y + BALL_RADIUS
    )

    # Check trigger zone
    currently_inside = ZONE_X1 <= x <= ZONE_X2

    if currently_inside and not inside_zone:
        draw_name()

    inside_zone = currently_inside

    root.after(16, animate)  # ~60 FPS


animate()
root.mainloop()
