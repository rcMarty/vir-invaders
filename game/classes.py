# --- Entities ---
from .config import WIDTH, HEIGHT, BULLET_SPEED
import pygame

class Player:
    def __init__(self, img=None):
        self.image = img or pygame.Surface((50, 20), pygame.SRCALPHA)
        if img is None:
            pygame.draw.rect(self.image, (50, 200, 50), self.image.get_rect())
        self.w, self.h = self.image.get_size()
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))

    def move(self, dx):
        self.rect.x = max(0, min(WIDTH - self.w, self.rect.x + dx))

    def draw(self, surf):
        surf.blit(self.image, self.rect)

class Bullet:
    def __init__(self, x, y, img=None):
        self.image = img
        self.r = 4
        self.x = x
        self.y = y
        self.alive = True
        if self.image:
            self.rect = self.image.get_rect(center=(int(x), int(y)))
        else:
            self.rect = pygame.Rect(int(x - self.r), int(y - self.r), self.r * 2, self.r * 2)

    def update(self):
        self.y += BULLET_SPEED
        if self.image:
            self.rect.centery = int(self.y)
            if self.rect.bottom < 0:
                self.alive = False
        else:
            if self.y < -10:
                self.alive = False

    def draw(self, surf):
        if self.image:
            surf.blit(self.image, self.rect)
        else:
            pygame.draw.circle(surf, (255, 255, 0), (int(self.x), int(self.y)), self.r)

class Enemy:
    def __init__(self, x, y, img=None):
        self.image = img or pygame.Surface((40, 20), pygame.SRCALPHA)
        if img is None:
            pygame.draw.rect(self.image, (200, 50, 50), self.image.get_rect())
        self.rect = self.image.get_rect(topleft=(x, y))
        self.alive = True

    def draw(self, surf):
        surf.blit(self.image, self.rect)