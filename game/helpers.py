from config import font

def draw_text(surf, text, x, y, color=(255,255,255)):
    img = font.render(text, True, color)
    surf.blit(img, (x, y))
