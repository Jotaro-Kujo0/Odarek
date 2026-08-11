import math
import config

class ArmSimulator:
    """Visual arm that rotates toward the first detected object.
    Swap with a real stepper/servo driver (modules/motion/arm.py) later."""

    def __init__(self):
        self.angle = 0.0
        self.target_angle = 0.0
        self.target = None

    def track(self, detections=None, command=None):
        detections = detections or []
        command = command or ""
        if detections:
            cx, cy = detections[0]["center"]
            dx = cx - config.SCREEN_WIDTH // 2
            dy = cy - config.SCREEN_HEIGHT // 2
            self.target_angle = math.degrees(math.atan2(dx, -dy))
            self.target = (cx, cy)
        if command == "scan":
            self.target_angle = (self.target_angle + 30) % 360

    def render(self, surface, base=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)):
        try:
            import pygame
            diff = (self.target_angle - self.angle + 180) % 360 - 180
            self.angle += diff * 0.1  # smooth rotation
            rad = math.radians(self.angle)
            length = 140
            tip = (base[0] + length * math.sin(rad),
                   base[1] - length * math.cos(rad))
            pygame.draw.line(surface, (220, 220, 230), base, tip, 6)
            pygame.draw.circle(surface, (200, 200, 220), (int(tip[0]), int(tip[1])), 10)
            pygame.draw.circle(surface, (80, 130, 255), base, 18, 3)
        except ImportError:
            pass
