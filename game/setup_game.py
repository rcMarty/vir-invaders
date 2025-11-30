# python
import pygame
from classes import Player, Enemy, Bullet
from config import *
import os


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
        pygame.display.set_caption("Tiny Space Invaders")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        self.player_img = None
        self.enemy_img = None
        self.bullet_img = None
        self.load_assets()
        self.reset()

    def load_assets(self):
        # expected paths: assets/
        try:
            base = os.path.join(os.path.dirname(__file__), "assets")
            print("base:", base)
            player_png = os.path.join(base, "grinch_1709x2000.png")
            enemy_png = os.path.join(base, "present_512x512.png")
            bullet_png = os.path.join(base, "tree_480x480.png")
            if os.path.exists(player_png):
                self.player_img = pygame.image.load(player_png).convert_alpha()
                self.player_img = pygame.transform.scale(self.player_img, (50, 50))
            if os.path.exists(enemy_png):
                self.enemy_img = pygame.image.load(enemy_png).convert_alpha()
                self.enemy_img = pygame.transform.scale(self.enemy_img, (40, 50))
            if os.path.exists(bullet_png):
                self.bullet_img = pygame.image.load(bullet_png).convert_alpha()
                self.bullet_img = pygame.transform.scale(self.bullet_img, (16, 16))
        except Exception as e:
            # If loading fails, keep images None -> shapes will be used
            print("Error loading assets:", e)
            self.player_img = None
            self.enemy_img = None
            self.bullet_img = None

    def reset(self):
        self.player = Player(self.player_img)
        self.bullets = []
        self.enemies = []
        self.start_x = (WIDTH - (COLS - 1) * ENEMY_PADDING) // 2
        for row in range(ROWS):
            for col in range(COLS):
                x = self.start_x + col * ENEMY_PADDING
                y = 50 + row * 50
                self.enemies.append(Enemy(x, y, self.enemy_img))
        self.enemy_dx = ENEMY_SPEED_X
        self.score = 0
        self.game_over = False


    def draw_text(self, text, x, y, color=(255, 255, 255)):
        img = self.font.render(text, True, color)
        self.screen.blit(img, (x, y))


    def player_shoot(self):
        self.bullets.append(Bullet(self.player.rect.centerx, self.player.rect.top, self.bullet_img))