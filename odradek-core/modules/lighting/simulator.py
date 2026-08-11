import config

class LEDSimulator:
    """Simulates the Odradek LED ring (blue = calm, orange = alert, red = danger).
    Swap the internals for a real WS2812/NeoPixel driver later."""

    def __init__(self):
        self.state = "calm"
        self.color = (80, 130, 255)
        self.speed = 1.0
        self.pulse = 0.0

    def set_state(self, detections=None, command=None):
        detections = detections or []
        command = command or ""

        if command == "scan":
            self.state = "scanning"
            self.color = (120, 200, 255)
            self.speed = 2.0
        elif command == "lights":
            self.state = "alert"
            self.color = (255, 170, 40)
            self.speed = 1.5
        elif command in ("danger", "bt"):
            self.state = "danger"
            self.color = (255, 40, 40)
            self.speed = 3.0
        else:
            big = any(d.get("confidence", 0) >= config.CONFIDENCE_THRESHOLD
                      for d in detections)
            self.state = "danger" if big else "calm"
            self.color = (255, 40, 40) if big else (80, 130, 255)
            self.speed = 3.0 if big else 1.0

    def render(self, surface, center, radius):
        """Draw the LED ring on a Pygame surface."""
        try:
            import pygame
            import math
            self.pulse = (self.pulse + 0.1 * self.speed) % (2 * math.pi)
            glow = int(60 + 60 * (0.5 + 0.5 * math.sin(self.pulse)))
            color = tuple(min(255, c + glow // 3) for c in self.color)
            pygame.draw.circle(surface, color, center, radius, 4)
        except ImportError:
            pass  # Pygame not installed — just track state

    def get_state(self):
        return {"state": self.state, "color": self.color, "speed": self.speed}
