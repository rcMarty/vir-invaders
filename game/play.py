import sys
from .classes import *
from .setup_game import Game
from .config import *


def play():
    def _draw_outlined_text(surf, text, x, y, font, color=(255, 255, 255), outline_color=(0, 0, 0),
                            outline_width=2):
        outline_surf = font.render(text, True, outline_color)
        text_surf = font.render(text, True, color)
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx == 0 and dy == 0:
                    continue
                surf.blit(outline_surf, (x + dx, y + dy))
        surf.blit(text_surf, (x, y))

    game = Game()
    while True:
        dt = game.clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if not game.game_over:
            if keys[pygame.K_LEFT]:
                game.player.move(-PLAYER_SPEED)
            if keys[pygame.K_RIGHT]:
                game.player.move(PLAYER_SPEED)
            if keys[pygame.K_SPACE]:
                if not game.bullets or game.bullets[-1].y < game.player.rect.top - BULLET_TIMEOUT:
                    game.player_shoot()

        for b in game.bullets:
            b.update()
        game.bullets = [b for b in game.bullets if b.alive]

        if not game.game_over:
            edge_hit = False
            for enemy in game.enemies:
                enemy.rect.x += game.enemy_dx
                if enemy.rect.right >= WIDTH or enemy.rect.left <= 0:
                    edge_hit = True
            if edge_hit:
                game.enemy_dx = -game.enemy_dx
                for enemy in game.enemies:
                    enemy.rect.y += ENEMY_DROP

        for b in game.bullets:
            for enemy in game.enemies:
                if enemy.alive and b.alive and enemy.rect.collidepoint(b.x, b.y):
                    enemy.alive = False
                    b.alive = False
                    game.score += 10

        game.enemies = [e for e in game.enemies if e.alive]

        for enemy in game.enemies:
            if enemy.rect.bottom >= game.player.rect.top:
                game.game_over = True
        if not game.enemies:
            game.game_over = True

        # draw background if available, otherwise clear to a solid color
        if getattr(game, 'bg_img', None):
            game.screen.blit(game.bg_img, (0, 0))
        else:
            game.screen.fill((10, 10, 30))
        game.player.draw(game.screen)
        for b in game.bullets:
            b.draw(game.screen)
        for enemy in game.enemies:
            enemy.draw(game.screen)

        font = getattr(game, 'font', pygame.font.SysFont(None, 36))

        _draw_outlined_text(game.screen, f"Score: {game.score}", 10, 10, font)
        if game.game_over:
            msg = "You Win!" if not game.enemies else "Game Over"
            _draw_outlined_text(game.screen, msg, WIDTH // 2 - 80, HEIGHT // 2 - 20, font, color=(255, 255, 0))
            _draw_outlined_text(game.screen, "Press R to restart or Esc to quit", WIDTH // 2 - 200, HEIGHT // 2 + 20,
                                font, color=(180, 180, 180))
            game.draw_text("Press R to restart or Esc to quit", WIDTH // 2 - 200, HEIGHT // 2 + 20, (180, 180, 180))
            if keys[pygame.K_r]:
                game.reset()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
