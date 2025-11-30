# python
import sys
import pygame

from config import *


# --- Config ---


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tiny Space Invaders")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)



class Enemy:
    def __init__(self, x, y):
        self.w, self.h = 40, 20
        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.alive = True

    def draw(self, surf):
        pygame.draw.rect(surf, (200, 50, 50), self.rect)

# --- Setup game objects ---
player = Player()
bullets = []
enemies = []
start_x = (WIDTH - (COLS - 1) * ENEMY_PADDING) // 2
for row in range(ROWS):
    for col in range(COLS):
        x = start_x + col * ENEMY_PADDING
        y = 50 + row * 50
        enemies.append(Enemy(x, y))

enemy_dx = ENEMY_SPEED_X
score = 0
game_over = False

# --- Helper ---
def draw_text(surf, text, x, y, color=(255,255,255)):
    img = font.render(text, True, color)
    surf.blit(img, (x, y))

# --- Main loop ---
while True:
    dt = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT]:
            player.move(-PLAYER_SPEED)
        if keys[pygame.K_RIGHT]:
            player.move(PLAYER_SPEED)
        if keys[pygame.K_SPACE]:
            # simple cooldown: only one bullet at a time
            if not bullets or bullets[-1].y < player.y - 50:
                bullets.append(Bullet(player.rect.centerx, player.rect.top))

    # update bullets
    for b in bullets:
        b.update()
    bullets = [b for b in bullets if b.alive]

    # update enemies
    if not game_over:
        edge_hit = False
        for e in enemies:
            e.rect.x += enemy_dx
            if e.rect.right >= WIDTH or e.rect.left <= 0:
                edge_hit = True
        if edge_hit:
            enemy_dx = -enemy_dx
            for e in enemies:
                e.rect.y += ENEMY_DROP

    # collisions
    for b in bullets:
        for e in enemies:
            if e.alive and b.alive and e.rect.collidepoint(b.x, b.y):
                e.alive = False
                b.alive = False
                score += 10

    enemies = [e for e in enemies if e.alive]

    # check lose/win
    for e in enemies:
        if e.rect.bottom >= player.rect.top:
            game_over = True
    if not enemies:
        game_over = True

    # draw
    screen.fill((10, 10, 30))
    player.draw(screen)
    for b in bullets:
        b.draw(screen)
    for e in enemies:
        e.draw(screen)
