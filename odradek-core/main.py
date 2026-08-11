import config
import pygame
import cv2
from modules.vision.detector import Detector
from modules.voice.wake_word import WakeWordListener
from modules.voice.commander import Commander
from modules.motion.simulator import ArmSimulator
from modules.lighting.simulator import LEDSimulator
from modules.heads.registry import HeadRegistry


def main():
    print("=== ODRADEK CORE v0.1 ===")
    print(f"Mode: {'SIMULATION' if config.SIMULATION_MODE else 'HARDWARE'}")

    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Odradek Simulator")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    detector = Detector()
    wake = WakeWordListener()
    commander = Commander()
    arm = ArmSimulator()
    leds = LEDSimulator()
    heads = HeadRegistry()

    running = True
    listening = False
    command = None

    while running:
        # ---- events ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # ---- sensing (each wrapped so one failure can't kill rendering) ----
        try:
            frame, detections = detector.update()
        except Exception:
            frame, detections = None, []

        if config.ENABLE_VOICE:
            try:
                if wake.detect():
                    listening = True
                    print("Listening for command...")
            except Exception:
                pass

            if listening:
                try:
                    command = commander.listen()
                    if command:
                        print(f"Command: {command}")
                        listening = False
                except Exception:
                    command = None

        arm.track(detections, command)
        leds.set_state(detections, command)

        # ---- draw (always) ----
        screen.fill((10, 10, 20))

        # Camera feed, top-left
        if frame is not None:
            try:
                small = cv2.resize(frame, (320, 240))
                small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
                surf = pygame.surfarray.make_surface(small.swapaxes(0, 1))
                screen.blit(surf, (10, 10))
            except Exception:
                pass

        # Arm + LED ring at screen center
        arm.render(screen)
        leds.render(screen, (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2), 24)

        # HUD
        status = font.render(
            f"Head: {heads.current.name} | Detections: {len(detections)} | "
            f"Command: {command or '---'} | FPS: {int(clock.get_fps())}",
            True, (180, 220, 255))
        screen.blit(status, (10, config.SCREEN_HEIGHT - 40))

        hint = font.render("ESC to quit | wake word then: scan / lights / danger",
                           True, (120, 140, 160))
        screen.blit(hint, (10, config.SCREEN_HEIGHT - 70))

        # ---- THE two lines that were probably missing ----
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    print("Shutdown complete.")


if __name__ == "__main__":
    main()
