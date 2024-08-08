import pygame
import random
import tkinter as tk
from tkinter import messagebox
import sys

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_WIDTH = 80
PIPE_GAP = 150

# Hard-coded credentials (use environment variables or a more secure method in production)
USERNAME = "user"
PASSWORD = "pass"

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = 300
        self.velocity = 0

    def flap(self):
        self.velocity += FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

# Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(150, 450)

    def update(self):
        self.x -= 5

    def draw(self):
        # Top pipe
        screen.blit(pipe_image, (self.x, self.height - SCREEN_HEIGHT))
        # Bottom pipe
        screen.blit(pipe_image, (self.x, self.height + PIPE_GAP))

def check_login():
    username = entry_username.get()
    password = entry_password.get()
    
    if username == USERNAME and password == PASSWORD:
        messagebox.showinfo("Login", "Login Successful!")
        login_window.destroy()
        start_game()
    else:
        messagebox.showerror("Login", "Invalid Credentials")

def start_game():
    # Initialize Pygame
    pygame.init()

    # Create the screen
    global screen, bird_image, pipe_image
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load images
    bird_image = pygame.Surface((30, 30))
    bird_image.fill((255, 0, 0))
    pipe_image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
    pipe_image.fill((0, 255, 0))

    # Game loop
    bird = Bird()
    pipes = [Pipe()]
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((135, 206, 235))  # Sky color

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.update()

        # Check for pipe generation
        if pipes[-1].x < SCREEN_WIDTH - 200:
            pipes.append(Pipe())

        for pipe in pipes:
            pipe.update()
            pipe.draw()

        # Draw the bird
        screen.blit(bird_image, (bird.x, bird.y))

        # Check for collisions
        for pipe in pipes:
            if bird.x + 30 > pipe.x and bird.x < pipe.x + PIPE_WIDTH:
                if bird.y < pipe.height or bird.y + 30 > pipe.height + PIPE_GAP:
                    running = False

        # If the bird falls below the screen
        if bird.y > SCREEN_HEIGHT or bird.y < 0:
            running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Create the login window
login_window = tk.Tk()
login_window.title("Login")

tk.Label(login_window, text="Username").pack()
entry_username = tk.Entry(login_window)
entry_username.pack()

tk.Label(login_window, text="Password").pack()
entry_password = tk.Entry(login_window, show='*')
entry_password.pack()

tk.Button(login_window, text="Login", command=check_login).pack()

login_window.mainloop()
