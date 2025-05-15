import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
FPS = 60
REEL_WIDTH = 80
REEL_HEIGHT = 80
REEL_COUNT = 3
SYMBOL_SIZE = 64
SYMBOLS = ['🍒', '🔔', '🍋', '💎', '7️⃣']  # Just for reference, we’ll use colored squares

# Colors (represent symbols)
SYMBOL_COLORS = {
    '🍒': (255, 0, 0),      # Red
    '🔔': (255, 255, 0),    # Yellow
    '🍋': (255, 255, 100),  # Light Yellow
    '💎': (0, 255, 255),    # Cyan
    '7️⃣': (255, 0, 255)    # Magenta
}

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pixel Slot Machine")
clock = pygame.time.Clock()

# Reel class
class Reel:
    def __init__(self, x):
        self.x = x
        self.symbols = [random.choice(SYMBOLS) for _ in range(5)]
        self.offset = 0
        self.speed = 0
        self.spinning = False

    def start_spin(self):
        self.speed = random.randint(20, 30)
        self.spinning = True

    def update(self):
        if self.spinning:
            self.offset += self.speed
            self.speed *= 0.95  # slow down gradually

            if self.speed < 1:
                self.spinning = False
                self.speed = 0
                self.offset = 0
                self.symbols = [random.choice(SYMBOLS) for _ in range(5)]

    def draw(self, surface):
        base_y = (SCREEN_HEIGHT - SYMBOL_SIZE) // 2
        for i in range(3):
            symbol_index = (i + int(self.offset // SYMBOL_SIZE)) % len(self.symbols)
            symbol = self.symbols[symbol_index]
            color = SYMBOL_COLORS[symbol]
            rect = pygame.Rect(self.x, base_y + i * SYMBOL_SIZE - int(self.offset) % SYMBOL_SIZE, REEL_WIDTH, SYMBOL_SIZE)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (0, 0, 0), rect, 2)  # border

# Initialize reels
reels = [Reel(50 + i * (REEL_WIDTH + 10)) for i in range(REEL_COUNT)]

# Main loop
running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Start spinning on spacebar
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            for reel in reels:
                reel.start_spin()

    # Update and draw reels
    for reel in reels:
        reel.update()
        reel.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
