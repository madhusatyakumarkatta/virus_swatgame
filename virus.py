import math
import random
import pygame

class Virus(pygame.sprite.Sprite):
    def __init__(self, target_pos, screen_w, screen_h, v_type="Normal", start_pos=None):
        super().__init__()
        self.v_type = v_type
        self.target_pos = target_pos # Commonly the center core
        
        # Determine start pos if not provided
        if start_pos is None:
            edge = random.randint(0, 3) # 0: top, 1: right, 2: bottom, 3: left
            if edge == 0:
                self.pos = [random.randint(0, screen_w), -50]
            elif edge == 1:
                self.pos = [screen_w + 50, random.randint(0, screen_h)]
            elif edge == 2:
                self.pos = [random.randint(0, screen_w), screen_h + 50]
            else:
                self.pos = [-50, random.randint(0, screen_h)]
        else:
            self.pos = list(start_pos)
            
        # Assign attributes based on type
        self.color: tuple[int, int, int] = (0, 255, 100)
        
        if v_type == "Normal":
            self.speed = 2.0
            self.hp = 1
            self.color = (0, 255, 100) # Bright Green
            self.radius = 20
            self.score_value = 10
        elif v_type == "Fast":
            self.speed = 4.5
            self.hp = 1
            self.color = (0, 255, 255) # Cyan
            self.radius = 16
            self.score_value = 20
        elif v_type == "Tank":
            self.speed = 1.0
            self.hp = 3
            self.color = (255, 50, 50) # Red
            self.radius = 35
            self.score_value = 50
        elif v_type == "Split":
            self.speed = 2.5
            self.hp = 1
            self.color = (200, 50, 255) # Purple
            self.radius = 25
            self.score_value = 15
        elif v_type == "Mini": # Spawned from Split
            self.speed = 5.0
            self.hp = 1
            self.color = (200, 50, 255)
            self.radius = 12
            self.score_value = 5
            
        self.active = True
        
    def update(self):
        if not self.active:
            return
            
        dx = self.target_pos[0] - self.pos[0]
        dy = self.target_pos[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        
        if dist > 0:
            nx = dx / dist
            ny = dy / dist
            self.pos[0] += nx * self.speed
            self.pos[1] += ny * self.speed
            
    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.active = False
            return True # Successfully destroyed
        return False
        
    def draw(self, surface):
        if self.active:
            pos_int = (int(self.pos[0]), int(self.pos[1]))
            # Neon glow effect
            pygame.draw.circle(surface, self.color, pos_int, self.radius)
            # Inner bright core
            pygame.draw.circle(surface, (255, 255, 255), pos_int, int(self.radius * 0.4))
            
            # Draw health indicator for Tank
            if self.hp > 1:
                pygame.draw.circle(surface, (0, 0, 0), pos_int, int(self.radius * 0.8), 2)