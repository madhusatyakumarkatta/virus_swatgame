import cv2
import pygame
import sys
from hand_tracking import HandTracker
from gesture_detection import GestureDetector
from game_logic import GameLogic
from ui import UI

def main():
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    SCREEN_WIDTH  = 1280
    SCREEN_HEIGHT = 720

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Virus Swat - Gesture Controlled")
    clock = pygame.time.Clock()

    # Initialize Core Modules
    hand_tracker     = HandTracker()
    gesture_detector = GestureDetector(swipe_threshold=60.0, hold_time=1.0)
    logic            = GameLogic(SCREEN_WIDTH, SCREEN_HEIGHT)
    ui_manager       = UI(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Initialize Webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open the webcam.")
        sys.exit()

    running      = True
    flash_frames = 0

    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # 2. Capture Webcam Frame
        success, frame = cap.read()
        if not success:
            continue

        # 3. Process Hand Tracking (OpenCV skin-detection based)
        idx_x, idx_y, is_open = hand_tracker.process_frame(frame, SCREEN_WIDTH, SCREEN_HEIGHT)
        current_pos = (idx_x, idx_y) if idx_x is not None else None

        # 4. Detect Gestures
        swipe_detected, swipe_line, is_shield = gesture_detector.update(current_pos, is_open)

        # 5. Global State Transitions (Start / Game Over)
        if logic.state == "START":
            if swipe_detected:
                logic.reset_game()
        elif logic.state == "GAMEOVER":
            if swipe_detected:
                logic.reset_game()

        # 6. Update Game Logic
        elif logic.state == "PLAYING":
            screen_flash = logic.update(swipe_line, is_shield)
            if screen_flash:
                flash_frames = 5

        # 7. Render
        ui_manager.render_frame(screen, logic, current_pos, swipe_line)

        # Screen flash effect on hit
        if flash_frames > 0:
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash_surface.set_alpha(100)
            flash_surface.fill((255, 0, 0))
            screen.blit(flash_surface, (0, 0))
            flash_frames -= 1

        pygame.display.flip()

        # 8. FPS cap (60 FPS)
        clock.tick(60)

    # Cleanup
    cap.release()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()