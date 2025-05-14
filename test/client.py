import pygame
import socket
import pickle
import math
import time

WIDTH, HEIGHT = 1500, 900
PLAYER_COLORS = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 165, 0)]
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.3.116", 5555))  # Change IP as needed
my_pos = pickle.loads(client.recv(1024))

def send_data(pos, projectiles):
    client.send(pickle.dumps({"pos": pos, "projectiles": projectiles}))
    return pickle.loads(client.recv(4096))

def shoot(pos, target):
    angle = math.atan2(target[1] - pos[1], target[0] - pos[0])
    speed = 10
    return [pos[0] + 25, pos[1] + 25, math.cos(angle) * speed, math.sin(angle) * speed]

bullets_to_send = []

run = True
while run:
    clock.tick(60)
    screen.fill((230, 230, 230))

    # Input
    keys = pygame.key.get_pressed()
    x, y = my_pos
    if keys[pygame.K_w]: y -= 5
    if keys[pygame.K_s]: y += 5
    if keys[pygame.K_a]: x -= 5
    if keys[pygame.K_d]: x += 5
    my_pos = (x, y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            bullets_to_send.append(shoot(my_pos, (mx, my)))

    # Send + receive data
    players, bullets, scores = send_data(my_pos, bullets_to_send)
    bullets_to_send = []

    # Draw tanks
    for i, p in enumerate(players):
        pygame.draw.rect(screen, PLAYER_COLORS[i], (*p, 50, 50))
        if p == my_pos:
            # Draw turret line
            mx, my = pygame.mouse.get_pos()
            pygame.draw.line(screen, (0, 0, 0), (p[0] + 25, p[1] + 25), (mx, my), 2)

    # Draw projectiles
    for b in bullets:
        pygame.draw.circle(screen, (0, 0, 0), (int(b[0]), int(b[1])), 5)

    # Draw score
    font = pygame.font.SysFont(None, 36)
    for i, s in enumerate(scores):
        screen.blit(font.render(f"P{i+1}: {s}", True, PLAYER_COLORS[i]), (20 + i * 100, 20))
        if s >= 5:
            win_text = font.render(f"Player {i+1} Wins!", True, (0, 0, 0))
            screen.blit(win_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.flip()

            # Countdown for restart
            for i in range(3, 0, -1):
                countdown_text = font.render(f"Restarting in {i}...", True, (0, 0, 0))
                screen.blit(countdown_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
                pygame.display.flip()
                time.sleep(1)
            # Restart game
            scores = [0] * len(players)
            players = [(100 + i * 100, 100) for i in range(len(players))]

    pygame.display.flip()

pygame.quit()
