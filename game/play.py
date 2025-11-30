import sys
from classes import *
from setup_game import Game
from config import *


def play():
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
                if not game.bullets or game.bullets[-1].y < game.player.rect.top - 50:
                    game.bullets.append(Bullet(game.player.rect.centerx, game.player.rect.top))

        for b in game.bullets:
            b.update()
        game.bullets = [b for b in game.bullets if b.alive]

        if not game.game_over:
            edge_hit = False
            for e in game.enemies:
                e.rect.x += game.enemy_dx
                if e.rect.right >= WIDTH or e.rect.left <= 0:
                    edge_hit = True
            if edge_hit:
                game.enemy_dx = -game.enemy_dx
                for e in game.enemies:
                    e.rect.y += ENEMY_DROP

        for b in game.bullets:
            for e in game.enemies:
                if e.alive and b.alive and e.rect.collidepoint(b.x, b.y):
                    e.alive = False
                    b.alive = False
                    game.score += 10

        game.enemies = [e for e in game.enemies if e.alive]

        for e in game.enemies:
            if e.rect.bottom >= game.player.rect.top:
                game.game_over = True
        if not game.enemies:
            game.game_over = True

        game.screen.fill((10, 10, 30))
        game.player.draw(game.screen)
        for b in game.bullets:
            b.draw(game.screen)
        for e in game.enemies:
            e.draw(game.screen)

        game.draw_text(f"Score: {game.score}", 10, 10)
        if game.game_over:
            msg = "You Win!" if not game.enemies else "Game Over"
            game.draw_text(msg, WIDTH // 2 - 80, HEIGHT // 2 - 20, (255, 255, 0))
            game.draw_text("Press R to restart or Esc to quit", WIDTH // 2 - 200, HEIGHT // 2 + 20, (180, 180, 180))
            if keys[pygame.K_r]:
                game.reset()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
