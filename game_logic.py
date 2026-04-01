import time
import math
import random
import pygame
from virus import Virus

class GameLogic:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.core_pos = (screen_w // 2, screen_h // 2)
        self.core_radius = 40
        
        self.state = "START"
        self.max_health = 100
        self.health = self.max_health
        self.score = 0
        self.combo = 1
        self.last_kill_time = 0.0
        self.power_meter = 0
        self.max_power = 100
        
        self.viruses = []
        self.particles = []
        
        self.spawn_timer = 0
        self.base_spawn_rate = 60 # Frames
        self.spawn_rate = self.base_spawn_rate
        
        self.shield_time_remaining = 0
        self.shield_max_time = 180 # 3 seconds at 60 fps
        
    def reset_game(self):
        self.health = self.max_health
        self.score = 0
        self.combo = 1
        self.power_meter = 0
        self.viruses = []
        self.particles = []
        self.spawn_rate = self.base_spawn_rate
        self.shield_time_remaining = 0
        self.state = "PLAYING"
        
    def get_difficulty_ratios(self):
        # Scale difficulty over time / score. Weights config
        score = self.score
        n_w = max(10, 80 - score // 20)
        f_w = min(40, 10 + score // 30)
        t_w = min(20, 5 + score // 50)
        s_w = min(25, 0 + score // 40)
        return [("Normal", n_w), ("Fast", f_w), ("Tank", t_w), ("Split", s_w)]
        
    def add_particle(self, pos, color):
        self.particles.append({"pos": pos, "radius": 5, "color": color, "alpha": 255})
        
    def update_particles(self):
        for p in self.particles:
            p["radius"] += 3
            p["alpha"] -= 15
        self.particles = [p for p in self.particles if p["alpha"] > 0]
        
    def get_distance_to_segment(self, point, p1, p2):
        x, y = point
        x1, y1 = p1
        x2, y2 = p2
        
        dx = x2 - x1
        dy = y2 - y1
        
        if dx == 0 and dy == 0:
            return math.hypot(x - x1, y - y1)
            
        t = ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)
        t = max(0, min(1, t))
        
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        
        return math.hypot(x - closest_x, y - closest_y)
        
    def update(self, swipe_line, is_shield_active):
        if self.state != "PLAYING":
            return False
            
        # Reset combo if too much time passes between kills
        if time.time() - self.last_kill_time > 2.0:
            self.combo = 1
            
        # Add new viruses based on spawn rate
        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            ratios = self.get_difficulty_ratios()
            types, weights = zip(*ratios)
            chosen_type = random.choices(types, weights=weights)[0]
            
            self.viruses.append(Virus(self.core_pos, self.screen_w, self.screen_h, chosen_type))
            
            # Subtly increase difficulty
            self.spawn_rate = max(15, self.base_spawn_rate - self.score // 50)
            self.spawn_timer = self.spawn_rate
            
        # Deploy shield if requested from gesture and energy gauge is full
        if is_shield_active and self.power_meter >= self.max_power and self.shield_time_remaining <= 0:
            self.shield_time_remaining = self.shield_max_time
            self.power_meter = 0
            
        if self.shield_time_remaining > 0:
            self.shield_time_remaining -= 1
            
        screen_flash = False
        
        for v in list(self.viruses):
            v.update()
            
            # Check proximity to core
            v_dx = v.pos[0] - self.core_pos[0]
            v_dy = v.pos[1] - self.core_pos[1]
            dist_to_core = math.hypot(v_dx, v_dy)
            
            # Condition 1: Virus Hit Core
            if dist_to_core < v.radius + self.core_radius:
                if self.shield_time_remaining > 0:
                    # Enemy bounces/destroyed by shield
                    v.hit()
                    self.add_particle(list(v.pos), (100, 200, 255))
                    self.score += v.score_value * self.combo
                else:
                    self.health -= 15
                    screen_flash = True
                    self.combo = 1
                    
                self.viruses.remove(v)
                if self.health <= 0:
                    self.state = "GAMEOVER"
                continue
                
            # Condition 2: Player Swiped Virus
            if swipe_line:
                dist_to_swipe = self.get_distance_to_segment(v.pos, swipe_line[0], swipe_line[1])
                # Larger collision box for better gameplay 'feel'
                if dist_to_swipe < v.radius + 15: 
                    destroyed = v.hit()
                    if destroyed:
                        self.add_particle(list(v.pos), v.color)
                        self.score += v.score_value * self.combo
                        self.combo += 1
                        self.last_kill_time = time.time()
                        self.power_meter = min(self.max_power, self.power_meter + 5)
                        
                        if v.v_type == "Split":
                            # Create Mini clones
                            for _ in range(2):
                                # Perturb the mini pos slightly so they split naturally
                                perturb_x = v.pos[0] + random.randint(-15, 15)
                                perturb_y = v.pos[1] + random.randint(-15, 15)
                                v_clone = Virus(self.core_pos, self.screen_w, self.screen_h, "Mini", start_pos=(perturb_x, perturb_y))
                                self.viruses.append(v_clone)
                                
                        self.viruses.remove(v)
                        
        self.update_particles()
        return screen_flash