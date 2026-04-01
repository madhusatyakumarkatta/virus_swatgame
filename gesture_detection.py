import math
import time

class GestureDetector:
    def __init__(self, swipe_threshold=50.0, hold_time=1.0):
        # swipe_threshold defines the minimum pixel velocity between frames to trigger a swipe
        self.swipe_threshold = swipe_threshold
        # hold_time defines how long palm must be open to activate shield
        self.hold_time = hold_time
        
        self.prev_pos = None
        self.prev_time = time.time()
        
        self.hold_start_time = None
        self.shield_active = False

    def update(self, current_pos, is_open_palm):
        current_time = time.time()
        dt = current_time - self.prev_time
        self.prev_time = current_time
        
        swipe_detected = False
        swipe_line = None # Will store (start_pos, end_pos) if a swipe happened
        
        if current_pos is not None:
            if self.prev_pos is not None and dt > 0:
                dx = current_pos[0] - self.prev_pos[0]
                dy = current_pos[1] - self.prev_pos[1]
                distance = math.hypot(dx, dy)
                
                # Calculate pixel distance. Pygame might run at 60 FPS.
                # Distance per frame is enough.
                if distance > self.swipe_threshold:
                    swipe_detected = True
                    swipe_line = (self.prev_pos, current_pos)
                    
            self.prev_pos = current_pos
        else:
            self.prev_pos = None
            
        # Hold detection for shield
        if is_open_palm and current_pos is not None:
            if self.hold_start_time is None:
                self.hold_start_time = current_time
            elif current_time - self.hold_start_time > self.hold_time:
                self.shield_active = True
        else:
            self.hold_start_time = None
            self.shield_active = False
            
        return swipe_detected, swipe_line, self.shield_active