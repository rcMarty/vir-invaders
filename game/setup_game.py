# python
import pygame
from classes import Player, Enemy
from config import *


class Game:
    def __init__(self):
        self.game_over = None
        self.score = None
        self.enemy_dx = None
        self.start_x = None
        self.enemies = None
        self.bullets = None
        self.player = None

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tiny Vir Christmas Invaders")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.reset()


    def reset(self):
        self.player = Player()
        self.bullets = []
        self.enemies = []
        self.start_x = (WIDTH - (COLS - 1) * ENEMY_PADDING) // 2
        for row in range(ROWS):
            for col in range(COLS):
                x = self.start_x + col * ENEMY_PADDING
                y = 50 + row * 50
                self.enemies.append(Enemy(x, y))
        self.enemy_dx = ENEMY_SPEED_X
        self.score = 0
        self.game_over = False


    def draw_text(self, text, x, y, color=(255, 255, 255)):
        img = self.font.render(text, True, color)
        self.screen.blit(img, (x, y))
