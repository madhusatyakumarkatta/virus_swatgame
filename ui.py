import pygame
import math
import time

class UI:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        pygame.font.init()
        self.font = pygame.font.SysFont("Courier", 32, bold=True)
        self.title_font = pygame.font.SysFont("Courier", 64, bold=True)
        
        # Grid Setup for Background
        self.bg_color = (13, 17, 23)
        self.grid_color = (25, 40, 50)
        self.grid_size = 60
        
    def draw_bg(self, surface):
        surface.fill(self.bg_color)
        
        # Draw techy grid
        for x in range(0, self.screen_w, self.grid_size):
            pygame.draw.line(surface, self.grid_color, (x, 0), (x, self.screen_h))
        for y in range(0, self.screen_h, self.grid_size):
            pygame.draw.line(surface, self.grid_color, (0, y), (self.screen_w, y))
            
    def draw_start_screen(self, surface):
        self.draw_bg(surface)
        title = self.title_font.render("VIRUS SWAT", True, (0, 255, 100))
        surface.blit(title, (self.screen_w//2 - title.get_width()//2, self.screen_h//3))
        
        sub = self.font.render("--- Swipe Fast to Start ---", True, (200, 255, 200))
        surface.blit(sub, (self.screen_w//2 - sub.get_width()//2, self.screen_h//2))
        
        inst = pygame.font.SysFont("Courier", 24).render("Swipe to attack. Open palm when gauge is full to shield.", True, (150, 150, 150))
        surface.blit(inst, (self.screen_w//2 - inst.get_width()//2, self.screen_h//2 + 60))
        
    def draw_game_over(self, surface, score):
        self.draw_bg(surface)
        title = self.title_font.render("SYSTEM BREACHED", True, (255, 50, 50))
        surface.blit(title, (self.screen_w//2 - title.get_width()//2, self.screen_h//3))
        
        sub = self.font.render(f"Final Score: {score}", True, (200, 200, 200))
        surface.blit(sub, (self.screen_w//2 - sub.get_width()//2, self.screen_h//2))
        
        restart = self.font.render("--- Swipe Fast to Restart ---", True, (100, 100, 100))
        surface.blit(restart, (self.screen_w//2 - restart.get_width()//2, self.screen_h//2 + 80))
        
    def draw_hud(self, surface, logic):
        # Health Bar - Top Center
        bar_w = 400
        bar_h = 24
        x = self.screen_w // 2 - bar_w // 2
        y = 30
        pygame.draw.rect(surface, (100, 0, 0), (x, y, bar_w, bar_h))
        hp_ratio = max(0, logic.health / logic.max_health)
        pygame.draw.rect(surface, (0, 255, 100), (x, y, int(bar_w * hp_ratio), bar_h))
        pygame.draw.rect(surface, (255, 255, 255), (x, y, bar_w, bar_h), 2)
        
        # Score - Top Left
        score_txt = self.font.render(f"SCORE: {logic.score}", True, (0, 255, 255))
        surface.blit(score_txt, (30, 20))
        
        # Combo - Top Right
        combo_color = (255, 255, 50) if logic.combo >= 5 else ((200, 200, 200) if logic.combo > 1 else (100, 100, 100))
        combo_txt = self.font.render(f"COMBO x{logic.combo}", True, combo_color)
        surface.blit(combo_txt, (self.screen_w - 200 - (logic.combo*2), 20)) # Small shake scaling 
        
        # Power Meter - Bottom Center
        pb_w = 300
        pb_h = 12
        px = self.screen_w // 2 - pb_w // 2
        py = self.screen_h - 40
        pygame.draw.rect(surface, (50, 50, 50), (px, py, pb_w, pb_h))
        power_ratio = min(1.0, logic.power_meter / logic.max_power)
        pygame.draw.rect(surface, (255, 100, 255), (px, py, int(pb_w * power_ratio), pb_h))
        
        if logic.power_meter >= logic.max_power:
            ready_txt = self.font.render("SHIELD READY [HOLD PALM OPEN]", True, (255, 100, 255))
            surface.blit(ready_txt, (self.screen_w//2 - ready_txt.get_width()//2, py - 40))
            
    def draw_core(self, surface, logic):
        color = (100, 100, 255)
        core_rad = logic.core_radius + math.sin(time.time() * 5) * 2 # Slight pulsing
        
        if logic.shield_time_remaining > 0:
            # Shield effect
            color = (100, 255, 255)
            shield_rad = core_rad + 20 + math.sin(time.time() * 20) * 5
            pygame.draw.circle(surface, color, logic.core_pos, int(shield_rad), 4)
            
        pygame.draw.circle(surface, color, logic.core_pos, int(core_rad))
        pygame.draw.circle(surface, (255, 255, 255), logic.core_pos, int(core_rad*0.5))
        
    def draw_particles(self, surface, logic):
        for p in logic.particles:
            s_color = (*p["color"], p["alpha"])
            rad = int(p["radius"])
            if rad <= 0: continue
            # create temporary surface for alpha
            part_surface = pygame.Surface((rad*2, rad*2), pygame.SRCALPHA)
            pygame.draw.circle(part_surface, s_color, (rad, rad), rad, max(1, rad//4))
            surface.blit(part_surface, (int(p["pos"][0]) - rad, int(p["pos"][1]) - rad))
            
    def render_frame(self, surface, logic, finger_pos, swipe_line):
        if logic.state == "START":
            self.draw_start_screen(surface)
        elif logic.state == "GAMEOVER":
            self.draw_game_over(surface, logic.score)
        else:
            self.draw_bg(surface)
            self.draw_core(surface, logic)
            self.draw_particles(surface, logic)
            
            for v in logic.viruses:
                v.draw(surface)
                
            self.draw_hud(surface, logic)
            
        # Draw Player Cursor / Swipe Trail
        if finger_pos:
            pygame.draw.circle(surface, (255, 255, 255), (int(finger_pos[0]), int(finger_pos[1])), 8)
            # Add a slight neon glow to cursor
            pygame.draw.circle(surface, (0, 255, 255), (int(finger_pos[0]), int(finger_pos[1])), 15, 2)
            
            if swipe_line:
                pygame.draw.line(surface, (0, 255, 255), 
                                 (int(swipe_line[0][0]), int(swipe_line[0][1])), 
                                 (int(swipe_line[1][0]), int(swipe_line[1][1])), 10)