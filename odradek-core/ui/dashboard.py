import config
import pygame


class Dashboard:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 22)
        self.bg_color = (15, 15, 30, 180)

    def draw(self, screen, head_registry, detections, command, fps):
        sidebar_x = config.SCREEN_WIDTH - 280
        sidebar_w = 270

        # sidebar
        s = pygame.Surface((sidebar_w, config.SCREEN_HEIGHT))
        s.set_alpha(180)
        s.fill(self.bg_color[:3])
        screen.blit(s, (sidebar_x, 0))

        y = 20

        # Title
        title = self.font_large.render("ODRADEK", True, (100, 200, 255))
        screen.blit(title, (sidebar_x + 15, y))
        y += 40

        # Head info
        if head_registry.current:
            label = self.font_small.render("Active Head:", True, (180, 180, 200))
            screen.blit(label, (sidebar_x + 15, y))
            y += 22
            name = self.font_large.render(head_registry.current.name.upper(), True, (255, 220, 100))
            screen.blit(name, (sidebar_x + 15, y))
            y += 35

        # Detection
        detect_label = self.font_small.render(f"Detections: {len(detections)}", True, (180, 220, 255))
        screen.blit(detect_label, (sidebar_x + 15, y))
        y += 25

        for d in detections[:5]:
            text = f"  {d['label']} ({d['confidence']:.2f})"
            item = self.font_small.render(text, True, (200, 200, 200))
            screen.blit(item, (sidebar_x + 15, y))
            y += 20

        # Command
        y += 10
        cmd_label = self.font_small.render(f"Command: {command or '---'}", True, (180, 255, 180))
        screen.blit(cmd_label, (sidebar_x + 15, y))
        y += 30

        # FPS
        fps_text = self.font_small.render(f"FPS: {fps:.0f}", True, (150, 150, 150))
        screen.blit(fps_text, (sidebar_x + 15, config.SCREEN_HEIGHT - 40))

        # Mode
        mode_text = self.font_small.render(f"Mode: {'SIM' if config.SIMULATION_MODE else 'HW'}", True, (150, 150, 150))
        screen.blit(mode_text, (sidebar_x + 15, config.SCREEN_HEIGHT - 65))
