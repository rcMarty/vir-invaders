# --- Entities ---
from config import WIDTH, HEIGHT, BULLET_SPEED
import pygame

class Player:
    def __init__(self):
        self.w, self.h = 50, 20
        self.x = (WIDTH - self.w) // 2
        self.y = HEIGHT - self.h - 10
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def move(self, dx):
        self.rect.x = max(0, min(WIDTH - self.w, self.rect.x + dx))

    def draw(self, surf):
        pygame.draw.rect(surf, (50, 200, 50), self.rect)

class Bullet:
    def __init__(self, x, y):
        self.r = 4
        self.x = x
        self.y = y
        self.alive = True

    def update(self):
        self.y += BULLET_SPEED
        if self.y < -10:
            self.alive = False

    def draw(self, surf):
        pygame.draw.circle(surf, (255, 255, 0), (int(self.x), int(self.y)), self.r)



class Enemy:
    def __init__(self, x, y):
        self.w, self.h = 40, 20
        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.alive = True

    def draw(self, surf):
        pygame.draw.rect(surf, (200, 50, 50), self.rect)
