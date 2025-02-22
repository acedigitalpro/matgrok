import pygame
import random

# Initialize Pygame
pygame.init()

# Initial windowed settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Matrix Rain with Xi and Grok - Full Screen Toggle")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Font (size will scale with screen)
font_size = 20
font = pygame.font.SysFont("courier", font_size, bold=True)

# Words to drop
WORDS = ["Xi", "Grok"]

# Drop class with spaced trail and dynamic sizing
class Drop:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = random.randint(0, self.screen_width - font_size)
        self.y = random.randint(-self.screen_height, 0)
        self.speed = random.uniform(1, 5)
        self.text = random.choice(WORDS)
        self.trail = []
        self.last_trail_y = self.y

    def update_screen_size(self, screen_width, screen_height):
        # Adjust x-position if screen size changes
        self.screen_width = screen_width
        self.screen_height = screen_height
        if self.x > self.screen_width - font_size:
            self.x = random.randint(0, self.screen_width - font_size)

    def fall(self):
        self.y += self.speed
        # Add trail position only if moved enough (20 pixels)
        if abs(self.y - self.last_trail_y) >= 20:
            surface = font.render(self.text, True, GREEN)
            self.trail.append((self.x, self.y, surface))
            self.last_trail_y = self.y
        
        # Reset when off-screen
        if self.y > self.screen_height:
            self.y = random.randint(-self.screen_height, 0)
            self.x = random.randint(0, self.screen_width - font_size)
            self.text = random.choice(WORDS)
            self.trail = []
            self.last_trail_y = self.y

    def draw(self):
        # Draw trail with fading effect
        for i, (x, y, surface) in enumerate(self.trail):
            alpha = int(255 * (1 - (self.y - y) / self.screen_height)) if self.y > y else 255
            if alpha < 0:
                alpha = 0
            trail_surface = surface.copy()
            trail_surface.set_alpha(max(50, alpha - 50))  # Dimmer trail
            screen.blit(trail_surface, (x, y))
        
        # Draw current word at full opacity
        current_surface = font.render(self.text, True, GREEN)
        current_surface.set_alpha(255)
        screen.blit(current_surface, (self.x, self.y))

# Initial setup
current_width, current_height = WINDOW_WIDTH, WINDOW_HEIGHT
drops = [Drop(current_width, current_height) for _ in range(50)]
is_fullscreen = False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:  # Press 'F' to toggle full screen
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    current_width, current_height = screen.get_width(), screen.get_height()
                else:
                    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
                    current_width, current_height = WINDOW_WIDTH, WINDOW_HEIGHT
                # Update drops for new screen size
                for drop in drops:
                    drop.update_screen_size(current_width, current_height)
        elif event.type == pygame.VIDEORESIZE and not is_fullscreen:
            # Handle manual window resizing
            current_width, current_height = event.w, event.h
            screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
            for drop in drops:
                drop.update_screen_size(current_width, current_height)

    # Clear screen
    screen.fill(BLACK)

    # Update and draw drops
    for drop in drops:
        drop.fall()
        drop.draw()

    # Update display
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()