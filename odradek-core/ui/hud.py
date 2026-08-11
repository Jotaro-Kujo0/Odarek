import pygame


class HUD:
    def __init__(self):
        self.font = pygame.font.Font(None, 20)

    def draw_text(self, screen, text, x, y, color=(200, 200, 200)):
        surface = self.font.render(text, True, color)
        screen.blit(surface, (x, y))

    def draw_bar(self, screen, x, y, width, height, value, max_val, color):
        """Draw a horizontal progress bar."""
        
        pygame.draw.rect(screen, (40, 40, 40), (x, y, width, height))
        fill_w = int(width * (value / max_val))
        fill_w = max(0, min(width, fill_w))
        if fill_w > 0:
            pygame.draw.rect(screen, color, (x, y, fill_w, height))
        pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height), 1)

    def draw_crosshair(self, screen, x, y, size=15, color=(255, 255, 255)):
        pygame.draw.line(screen, color, (x - size, y), (x + size, y), 1)
        pygame.draw.line(screen, color, (x, y - size), (x, y + size), 1)
        pygame.draw.circle(screen, color, (x, y), size, 1)

    def draw_status_led(self, screen, x, y, radius, on, color_on=(0, 255, 0), color_off=(60, 60, 60)):
        color = color_on if on else color_off
        pygame.draw.circle(screen, color, (x, y), radius)
        if on:
            pygame.draw.circle(screen, (255, 255, 255), (x, y), radius // 3)
