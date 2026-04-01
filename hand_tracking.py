import cv2
import numpy as np
import math

class HandTracker:
    """
    OpenCV-based hand tracker using skin color detection + convexity defects.
    No MediaPipe needed — works with Python 3.14+.

    DEBUG WINDOW:
    - A small window titled "Hand Tracking Debug" will appear beside the game.
    - LEFT  = camera feed with green contour and red dot on fingertip
    - RIGHT = skin mask (white = detected as skin)
    - Text overlay shows: HAND DETECTED/NO HAND, finger count, SHIELD ON/OFF
    """

    def __init__(self, debug=True):
        self.prev_x = 0
        self.prev_y = 0
        self.alpha  = 0.4
        self.debug  = debug  # Set to False to hide the debug window

    def _get_skin_mask(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_skin = np.array([0,  20,  70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)
        mask = cv2.erode(mask,   kernel, iterations=1)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        return mask

    def _count_fingers(self, contour):
        if contour is None or len(contour) < 10:
            return 0
        try:
            hull    = cv2.convexHull(contour, returnPoints=False)
            if hull is None or len(hull) < 3:
                return 0
            defects = cv2.convexityDefects(contour, hull)
        except Exception:
            return 0
        if defects is None:
            return 0
        count = 0
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(contour[s][0])
            end   = tuple(contour[e][0])
            far   = tuple(contour[f][0])
            a = math.dist(end, start)
            b = math.dist(far, start)
            c = math.dist(end, far)
            denom = 2 * b * c
            if denom == 0:
                continue
            angle = math.acos(max(-1.0, min(1.0, (b**2 + c**2 - a**2) / denom)))
            if angle <= math.pi / 2 and d > 10000:
                count += 1
        return min(5, count + 1)

    def _get_topmost_point(self, contour):
        if contour is None or len(contour) == 0:
            return None
        return tuple(contour[contour[:, :, 1].argmin()][0])

    def process_frame(self, frame, screen_w, screen_h):
        frame       = cv2.flip(frame, 1)
        h, w        = frame.shape[:2]
        debug_frame = frame.copy()

        mask        = self._get_skin_mask(frame)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        index_x, index_y = None, None
        is_open  = False
        fingers  = 0
        status   = "NO HAND"

        if contours:
            hand = max(contours, key=cv2.contourArea)
            if cv2.contourArea(hand) > 5000:
                status = "HAND DETECTED"
                cv2.drawContours(debug_frame, [hand], -1, (0, 255, 0), 2)

                tip = self._get_topmost_point(hand)
                if tip:
                    target_x = int(tip[0] * screen_w / w)
                    target_y = int(tip[1] * screen_h / h)
                    if self.prev_x == 0 and self.prev_y == 0:
                        self.prev_x, self.prev_y = target_x, target_y
                    index_x = int(self.alpha * target_x + (1 - self.alpha) * self.prev_x)
                    index_y = int(self.alpha * target_y + (1 - self.alpha) * self.prev_y)
                    self.prev_x, self.prev_y = index_x, index_y
                    cv2.circle(debug_frame, tip, 12, (0, 0, 255), -1)
                    cv2.putText(debug_frame, "CURSOR TIP", (tip[0]+15, tip[1]),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                fingers = self._count_fingers(hand)
                is_open = fingers >= 4

        if self.debug:
            status_color = (0, 255, 0) if status == "HAND DETECTED" else (0, 0, 255)
            cv2.putText(debug_frame, status,        (10, 30),  cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
            cv2.putText(debug_frame, f"Fingers: {fingers}", (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
            shield_label = "SHIELD: ON  (open palm)" if is_open else "SHIELD: OFF"
            shield_color = (255, 0, 255) if is_open else (120, 120, 120)
            cv2.putText(debug_frame, shield_label,  (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, shield_color, 2)
            cv2.putText(debug_frame, "Red dot = cursor tip", (10, h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), 1)

            mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            cv2.putText(mask_bgr, "SKIN MASK",          (10, 30),  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
            cv2.putText(mask_bgr, "White = skin region",(10, h-10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), 1)

            panel_w    = 480
            panel_h    = int(h * panel_w / w)
            left_panel = cv2.resize(debug_frame, (panel_w, panel_h))
            right_panel= cv2.resize(mask_bgr,    (panel_w, panel_h))
            combined   = np.hstack([left_panel, right_panel])
            cv2.imshow("Hand Tracking Debug", combined)
            cv2.waitKey(1)

        return index_x, index_y, is_open