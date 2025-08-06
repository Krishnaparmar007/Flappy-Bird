import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
BIRD_SIZE = 30
PIPE_WIDTH = 60
INITIAL_PIPE_GAP = 250  # Start with larger gap
MIN_PIPE_GAP = 150      # Minimum gap size
INITIAL_PIPE_SPEED = 1.5  # Start slower
MAX_PIPE_SPEED = 4.5      # Maximum speed
GRAVITY = 0.45
JUMP_STRENGTH = -8
PIPE_SPAWN_RATE = 5000  # milliseconds
FPS = 60

# Speed and gap progression settings
SPEED_INCREASE_RATE = 0.08  # How much speed increases per score point
GAP_DECREASE_RATE = 4       # How much gap decreases per score point

# Enhanced Colors with more variety
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (144, 238, 144)
BLUE = (135, 206, 235)
DARK_BLUE = (25, 25, 112)
YELLOW = (255, 215, 0)
BRIGHT_YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
DARK_ORANGE = (255, 140, 0)
RED = (220, 20, 60)
CRIMSON = (220, 20, 60)
GRAY = (128, 128, 128)
LIGHT_GRAY = (211, 211, 211)
DARK_GRAY = (64, 64, 64)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)
SHADOW = (50, 50, 50)
NEON_GREEN = (57, 255, 20)
NEON_BLUE = (30, 144, 255)
NEON_PINK = (255, 20, 147)
SUNSET_ORANGE = (255, 99, 71)
PURPLE = (147, 0, 211)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
LIME = (50, 205, 50)
RAINBOW_COLORS = [(255,0,0), (255,127,0), (255,255,0), (0,255,0), (0,0,255), (75,0,130), (148,0,211)]
PARTICLE_COLORS = [GOLD, BRIGHT_YELLOW, ORANGE, NEON_GREEN, NEON_BLUE, NEON_PINK, CYAN, MAGENTA]
STAR_COLORS = [WHITE, BRIGHT_YELLOW, CYAN, NEON_PINK]

# Background gradient colors for different times
DAY_COLORS = [(135, 206, 235), (176, 224, 230)]
SUNSET_COLORS = [(255, 94, 77), (255, 154, 0)]
NIGHT_COLORS = [(25, 25, 112), (72, 61, 139)]

class Particle:
    def __init__(self, x, y, color, velocity_x, velocity_y, life, particle_type="circle"):
        self.x = x
        self.y = y
        self.color = color
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.life = life
        self.max_life = life
        self.particle_type = particle_type
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5, 5)
        
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += 0.1  # Gravity on particles
        self.velocity_x *= 0.99  # Air resistance
        self.life -= 1
        self.rotation += self.rotation_speed
        
    def draw(self, screen):
        if self.life <= 0:
            return
            
        alpha_ratio = self.life / self.max_life
        alpha = int(255 * alpha_ratio)
        size = max(1, int(4 * alpha_ratio))
        
        if self.particle_type == "star":
            self.draw_star(screen, size, alpha_ratio)
        elif self.particle_type == "sparkle":
            self.draw_sparkle(screen, size, alpha_ratio)
        else:
            # Enhanced circle with glow
            glow_size = size + 2
            glow_color = (*self.color[:3], max(0, alpha // 3))
            
            # Create surface for glow effect
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, glow_color, (glow_size, glow_size), glow_size)
            screen.blit(glow_surf, (int(self.x - glow_size), int(self.y - glow_size)))
            
            # Main particle
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)
    
    def draw_star(self, screen, size, alpha_ratio):
        points = []
        for i in range(10):  # 5-pointed star
            angle = math.radians(i * 36 + self.rotation)
            radius = size * (2 if i % 2 == 0 else 1)
            x = self.x + math.cos(angle) * radius
            y = self.y + math.sin(angle) * radius
            points.append((x, y))
        
        if len(points) >= 3:
            pygame.draw.polygon(screen, self.color, points)
    
    def draw_sparkle(self, screen, size, alpha_ratio):
        # Draw cross-shaped sparkle
        length = size * 2
        pygame.draw.line(screen, self.color, 
                        (self.x - length, self.y), (self.x + length, self.y), 2)
        pygame.draw.line(screen, self.color, 
                        (self.x, self.y - length), (self.x, self.y + length), 2)
        
        # Diagonal lines for more sparkle
        diag_len = length * 0.7
        pygame.draw.line(screen, self.color,
                        (self.x - diag_len, self.y - diag_len), 
                        (self.x + diag_len, self.y + diag_len), 1)
        pygame.draw.line(screen, self.color,
                        (self.x - diag_len, self.y + diag_len), 
                        (self.x + diag_len, self.y - diag_len), 1)

class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT // 2)
        self.brightness = random.uniform(0.3, 1.0)
        self.twinkle_speed = random.uniform(0.02, 0.05)
        self.size = random.randint(1, 2)
        self.color = random.choice(STAR_COLORS)
        
    def update(self):
        self.brightness += math.sin(pygame.time.get_ticks() * self.twinkle_speed) * 0.1
        self.brightness = max(0.2, min(1.0, self.brightness))
        
    def draw(self, screen):
        alpha = int(255 * self.brightness)
        color_with_alpha = (*self.color[:3], alpha)
        
        # Create twinkling effect
        twinkle_surface = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)
        pygame.draw.circle(twinkle_surface, self.color, (self.size * 2, self.size * 2), self.size)
        
        # Add sparkle lines for brighter stars
        if self.brightness > 0.7:
            line_length = self.size * 3
            center = (self.size * 2, self.size * 2)
            pygame.draw.line(twinkle_surface, self.color,
                           (center[0] - line_length, center[1]), 
                           (center[0] + line_length, center[1]), 1)
            pygame.draw.line(twinkle_surface, self.color,
                           (center[0], center[1] - line_length), 
                           (center[0], center[1] + line_length), 1)
        
        screen.blit(twinkle_surface, (self.x - self.size * 2, self.y - self.size * 2))

class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.size = BIRD_SIZE
        self.angle = 0
        self.animation_frame = 0
        self.wing_flap = 0
        
    def jump(self):
        self.velocity = JUMP_STRENGTH
        self.wing_flap = 10
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
        # Update angle based on velocity for realistic rotation
        self.angle = min(30, max(-30, self.velocity * 3))
        
        # Wing flap animation
        self.animation_frame += 1
        if self.wing_flap > 0:
            self.wing_flap -= 1
            
    def draw_trail(self, screen):
        positions = [(self.x - i * 2, self.y + math.sin(i * 0.5 + pygame.time.get_ticks() * 0.01) * 3) 
                     for i in range(1, 15)]
        for i, pos in enumerate(positions):
            color = RAINBOW_COLORS[i % len(RAINBOW_COLORS)]
            alpha = 255 - (i * 15)
            if alpha > 0:
                trail_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
                pygame.draw.circle(trail_surf, (*color, alpha), (3, 3), 3)
                screen.blit(trail_surf, (pos[0] - 3, pos[1] - 3))

    def draw(self, screen):
        self.draw_trail(screen)  # Add this line at the start of the method
        # Create rotated bird surface
        bird_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        
        # Body (main circle with gradient effect)
        center_x, center_y = self.size, self.size
        
        # Shadow
        pygame.draw.circle(bird_surface, SHADOW, (center_x + 2, center_y + 2), self.size // 2)
        
        # Main body with gradient effect
        for i in range(self.size // 2, 0, -1):
            brightness = 1 - (i / (self.size // 2)) * 0.3
            body_color = (int(YELLOW[0] * brightness), int(YELLOW[1] * brightness), int(YELLOW[2] * brightness))
            pygame.draw.circle(bird_surface, body_color, (center_x, center_y), i)
        
        # Wing animation
        wing_offset = math.sin(self.animation_frame * 0.3) * 3 if self.wing_flap == 0 else -5
        wing_color = ORANGE if self.wing_flap > 0 else (255, 140, 0)
        
        # Wing
        wing_points = [
            (center_x - 8, center_y + wing_offset),
            (center_x - 15, center_y - 5 + wing_offset),
            (center_x - 12, center_y + 5 + wing_offset)
        ]
        pygame.draw.polygon(bird_surface, wing_color, wing_points)
        pygame.draw.polygon(bird_surface, BLACK, wing_points, 1)
        
        # Eye with highlight
        eye_x, eye_y = center_x + 5, center_y - 3
        pygame.draw.circle(bird_surface, WHITE, (eye_x, eye_y), 6)
        pygame.draw.circle(bird_surface, BLACK, (eye_x, eye_y), 4)
        pygame.draw.circle(bird_surface, WHITE, (eye_x - 1, eye_y - 1), 2)
        
        # Beak with gradient
        beak_points = [
            (center_x + self.size // 2 - 3, center_y),
            (center_x + self.size // 2 + 8, center_y - 2),
            (center_x + self.size // 2 + 8, center_y + 2)
        ]
        pygame.draw.polygon(bird_surface, ORANGE, beak_points)
        pygame.draw.polygon(bird_surface, RED, beak_points, 1)
        
        # Rotate the bird based on velocity
        rotated_bird = pygame.transform.rotate(bird_surface, -self.angle)
        bird_rect = rotated_bird.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_bird, bird_rect)
        
    def get_rect(self):
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, 
                          self.size, self.size)

class Pipe:
    def __init__(self, x, gap_size, speed):
        self.x = x
        self.gap_size = gap_size
        self.speed = speed
        self.height = random.randint(100, SCREEN_HEIGHT - gap_size - 100)
        self.passed = False
        
    def update(self):
        self.x -= self.speed
        
    def draw(self, screen):
        # Add pulsing glow effect
        time_pulse = math.sin(pygame.time.get_ticks() * 0.003) * 0.2 + 0.8
        glow_color = (int(NEON_GREEN[0] * time_pulse),
                     int(NEON_GREEN[1] * time_pulse),
                     int(NEON_GREEN[2] * time_pulse))
        
        # Draw glow
        glow_surface = pygame.Surface((PIPE_WIDTH + 10, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (*glow_color, 100), 
                        (0, 0, PIPE_WIDTH + 10, self.height), 5)
        pygame.draw.rect(glow_surface, (*glow_color, 100),
                        (0, self.height + self.gap_size, PIPE_WIDTH + 10, 
                         SCREEN_HEIGHT - self.height - self.gap_size), 5)
        screen.blit(glow_surface, (self.x - 5, 0))
        
        # Pipe gradient and 3D effect
        pipe_surface = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Top pipe
        for i in range(PIPE_WIDTH):
            brightness = 1 - (i / PIPE_WIDTH) * 0.3
            pipe_color = (int(GREEN[0] * brightness), int(GREEN[1] * brightness), int(GREEN[2] * brightness))
            pygame.draw.line(pipe_surface, pipe_color, (i, 0), (i, self.height))
            pygame.draw.line(pipe_surface, pipe_color, (i, self.height + self.gap_size), (i, SCREEN_HEIGHT))
        
        # Pipe borders
        pygame.draw.rect(pipe_surface, DARK_GREEN, (0, 0, PIPE_WIDTH, self.height), 2)
        pygame.draw.rect(pipe_surface, DARK_GREEN, (0, self.height + self.gap_size, PIPE_WIDTH, SCREEN_HEIGHT - self.height - self.gap_size), 2)
        
        # Pipe caps with 3D effect
        cap_height = 30
        cap_width = PIPE_WIDTH + 10
        
        # Top cap
        cap_rect = pygame.Rect(self.x - 5, self.height - cap_height, cap_width, cap_height)
        pygame.draw.rect(screen, GREEN, cap_rect)
        pygame.draw.rect(screen, DARK_GREEN, cap_rect, 2)
        # 3D highlight
        pygame.draw.line(screen, (100, 200, 100), (cap_rect.left + 2, cap_rect.top + 2), (cap_rect.right - 2, cap_rect.top + 2), 2)
        
        # Bottom cap
        cap_rect = pygame.Rect(self.x - 5, self.height + self.gap_size, cap_width, cap_height)
        pygame.draw.rect(screen, GREEN, cap_rect)
        pygame.draw.rect(screen, DARK_GREEN, cap_rect, 2)
        pygame.draw.line(screen, (100, 200, 100), (cap_rect.left + 2, cap_rect.top + 2), (cap_rect.right - 2, cap_rect.top + 2), 2)
        
        # Blit the pipe surface
        screen.blit(pipe_surface, (self.x, 0))
        
    def collides_with(self, bird):
        bird_rect = bird.get_rect()
        top_pipe = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        bottom_pipe = pygame.Rect(self.x, self.height + self.gap_size, 
                                 PIPE_WIDTH, SCREEN_HEIGHT - self.height - self.gap_size)
        return bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe)
        
    def is_off_screen(self):
        return self.x + PIPE_WIDTH < 0

class Cloud:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.uniform(0.2, 0.8)
        self.size = random.randint(20, 40)
        
    def update(self):
        self.x -= self.speed
        if self.x < -self.size:
            self.x = SCREEN_WIDTH + self.size
            self.y = random.randint(50, 200)
            
    def draw(self, screen):
        cloud_color = (255, 255, 255, 150)
        cloud_surface = pygame.Surface((self.size * 3, self.size * 2), pygame.SRCALPHA)
        
        # Draw multiple circles to create cloud shape
        pygame.draw.circle(cloud_surface, WHITE, (self.size // 2, self.size), self.size // 3)
        pygame.draw.circle(cloud_surface, WHITE, (self.size, self.size), self.size // 2)
        pygame.draw.circle(cloud_surface, WHITE, (self.size * 3 // 2, self.size), self.size // 3)
        pygame.draw.circle(cloud_surface, WHITE, (self.size * 2, self.size), self.size // 4)
        
        screen.blit(cloud_surface, (int(self.x), int(self.y)))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🐦 Enhanced Flappy Bird - Ultimate Edition")
        self.clock = pygame.time.Clock()
        
        # Fonts with better styling
        try:
            self.font = pygame.font.Font("freesansbold.ttf", 24)
            self.large_font = pygame.font.Font("freesansbold.ttf", 36)
            self.title_font = pygame.font.Font("freesansbold.ttf", 48)
        except:
            self.font = pygame.font.Font(None, 24)
            self.large_font = pygame.font.Font(None, 36)
            self.title_font = pygame.font.Font(None, 48)
            
        self.clouds = [Cloud(random.randint(0, SCREEN_WIDTH), random.randint(50, 200)) for _ in range(8)]
        self.stars = [Star() for _ in range(50)]
        self.particles = []
        self.score_pulse = 0
        self.title_bounce = 0
        self.background_time = 0
        self.combo_count = 0
        self.last_score_time = 0
        
        self.reset_game()
        
    def reset_game(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.game_started = False
        self.particles.clear()
        self.current_speed = INITIAL_PIPE_SPEED
        self.current_gap = INITIAL_PIPE_GAP
        
    def get_current_speed(self):
        # Gradually increase speed based on score
        speed = INITIAL_PIPE_SPEED + (self.score * SPEED_INCREASE_RATE)
        return min(speed, MAX_PIPE_SPEED)
    
    def get_current_gap(self):
        # Gradually decrease gap based on score
        gap = INITIAL_PIPE_GAP - (self.score * GAP_DECREASE_RATE)
        return max(gap, MIN_PIPE_GAP)
        
    def spawn_pipe(self):
        self.current_speed = self.get_current_speed()
        self.current_gap = self.get_current_gap()
        self.pipes.append(Pipe(SCREEN_WIDTH, self.current_gap, self.current_speed))
        
    def add_score_particles(self):
        # Enhanced score particles with different types
        current_time = pygame.time.get_ticks()
        
        # Check for combo scoring (multiple scores in quick succession)
        if current_time - self.last_score_time < 2000:  # Within 2 seconds
            self.combo_count += 1
        else:
            self.combo_count = 1
        
        self.last_score_time = current_time
        
        # More particles for combos
        particle_count = 20 + (self.combo_count * 5)
        
        for _ in range(particle_count):
            color = random.choice(PARTICLE_COLORS)
            particle_type = random.choice(["circle", "star", "sparkle"])
            
            # Special effects for high combos
            if self.combo_count >= 3:
                particle_type = "star"
                color = GOLD
            elif self.combo_count >= 2:
                particle_type = "sparkle"
                color = NEON_PINK
            
            self.particles.append(
                Particle(
                    self.bird.x + random.randint(-25, 25),
                    self.bird.y + random.randint(-25, 25),
                    color,
                    random.uniform(-4, 4),  # More spread for combos
                    random.uniform(-5, -1),
                    random.randint(40, 70),  # Longer lifetime for special effects
                    particle_type
                )
            )
    
    def add_collision_particles(self):
        for _ in range(30):
            color = random.choice([RED, ORANGE, YELLOW, CRIMSON])
            particle_type = random.choice(["circle", "sparkle"])
            
            self.particles.append(
                Particle(
                    self.bird.x + random.randint(-20, 20),
                    self.bird.y + random.randint(-20, 20),
                    color,
                    random.uniform(-5, 5),
                    random.uniform(-5, -1),
                    50,
                    particle_type
                )
            )
        
    def update(self):
        # Update background elements
        self.background_time += 0.01
        
        # Update clouds
        for cloud in self.clouds:
            cloud.update()
            
        # Update stars
        for star in self.stars:
            star.update()
            
        # Update particles
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
        
        # Update animations
        self.title_bounce += 0.1
        if self.score_pulse > 0:
            self.score_pulse -= 1
            
        if not self.game_over and self.game_started:
            self.bird.update()
            
            # Spawn pipes with dynamic spacing based on current speed
            pipe_spacing = max(200, int(300 - self.current_speed * 20))
            if len(self.pipes) == 0 or self.pipes[-1].x < SCREEN_WIDTH - pipe_spacing:
                self.spawn_pipe()
                
            # Update pipes
            for pipe in self.pipes[:]:
                pipe.update()
                if pipe.is_off_screen():
                    self.pipes.remove(pipe)
                    
                # Check for scoring
                if not pipe.passed and pipe.x + PIPE_WIDTH < self.bird.x:
                    pipe.passed = True
                    self.score += 1
                    self.score_pulse = 20
                    self.add_score_particles()
                    
                # Check collision
                if pipe.collides_with(self.bird):
                    self.game_over = True
                    self.add_collision_particles()
                    
            # Check ground/ceiling collision
            if self.bird.y > SCREEN_HEIGHT - BIRD_SIZE // 2 or self.bird.y < BIRD_SIZE // 2:
                if not self.game_over:
                    self.add_collision_particles()
                self.game_over = True
                
    def draw_text_with_shadow(self, text, font, color, shadow_color, x, y):
        shadow = font.render(text, True, shadow_color)
        main_text = font.render(text, True, color)
        self.screen.blit(shadow, (x + 2, y + 2))
        self.screen.blit(main_text, (x, y))
        return main_text.get_rect(x=x, y=y)
        
    def draw(self):
        # Enhanced animated sky gradient with smooth time-based transitions
        time_offset = pygame.time.get_ticks() * 0.00005  # Slower transition
        
        # Create smooth continuous cycle through different times of day
        time_cycle = (math.sin(time_offset) + 1) / 2  # 0 to 1, smoother cycle
        
        for y in range(SCREEN_HEIGHT):
            sky_progress = y / SCREEN_HEIGHT
            
            # Define color sets for different times
            day_colors = (135, 206, 235)
            sunset_colors = (255, 154, 77)
            evening_colors = (72, 61, 139)
            night_colors = (25, 25, 112)
            
            # Smooth interpolation between time periods
            if time_cycle <= 0.25:  # Day to Sunset
                blend = time_cycle * 4  # 0 to 1
                base_r = int(day_colors[0] * (1 - blend) + sunset_colors[0] * blend)
                base_g = int(day_colors[1] * (1 - blend) + sunset_colors[1] * blend)
                base_b = int(day_colors[2] * (1 - blend) + sunset_colors[2] * blend)
            elif time_cycle <= 0.5:  # Sunset to Evening
                blend = (time_cycle - 0.25) * 4  # 0 to 1
                base_r = int(sunset_colors[0] * (1 - blend) + evening_colors[0] * blend)
                base_g = int(sunset_colors[1] * (1 - blend) + evening_colors[1] * blend)
                base_b = int(sunset_colors[2] * (1 - blend) + evening_colors[2] * blend)
            elif time_cycle <= 0.75:  # Evening to Night
                blend = (time_cycle - 0.5) * 4  # 0 to 1
                base_r = int(evening_colors[0] * (1 - blend) + night_colors[0] * blend)
                base_g = int(evening_colors[1] * (1 - blend) + night_colors[1] * blend)
                base_b = int(evening_colors[2] * (1 - blend) + night_colors[2] * blend)
            else:  # Night to Day
                blend = (time_cycle - 0.75) * 4  # 0 to 1
                base_r = int(night_colors[0] * (1 - blend) + day_colors[0] * blend)
                base_g = int(night_colors[1] * (1 - blend) + day_colors[1] * blend)
                base_b = int(night_colors[2] * (1 - blend) + day_colors[2] * blend)
            
            # Add subtle variations for more natural look
            variation_r = math.sin(time_offset * 2 + sky_progress) * 10
            variation_g = math.cos(time_offset * 1.5 + sky_progress * 1.5) * 8
            variation_b = math.sin(time_offset * 1.8 + sky_progress * 2) * 12
            
            final_r = max(0, min(255, base_r + variation_r))
            final_g = max(0, min(255, base_g + variation_g))
            final_b = max(0, min(255, base_b + variation_b))
            
            color = (int(final_r), int(final_g), int(final_b))
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
        
        # Smooth star visibility transition
        # Stars become more visible during evening and night
        if time_cycle >= 0.4:  # Start showing stars during evening
            star_visibility = min(1.0, (time_cycle - 0.4) * 2.5)  # Gradual fade in
        else:
            star_visibility = max(0.0, (0.4 - time_cycle) * 0.5)  # Fade out during day
            
        for star in self.stars:
            if star_visibility > 0.1:
                # Adjust star brightness based on time of day
                original_brightness = star.brightness
                star.brightness *= star_visibility
                star.draw(self.screen)
                star.brightness = original_brightness  # Restore original brightness
        
        # Draw clouds
        for cloud in self.clouds:
            cloud.draw(self.screen)
            
        # Draw pipes with enhanced visuals
        for pipe in self.pipes:
            pipe.draw(self.screen)
            
        # Draw bird
        self.bird.draw(self.screen)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Enhanced score display 
        score_scale = 1 + (self.score_pulse / 40)
        score_font = pygame.font.Font(None, int(36 * score_scale))
        
        # Score background (smaller since we removed difficulty info)
        score_bg = pygame.Surface((140, 50))
        score_bg.set_alpha(150)
        score_bg.fill(BLACK)
        self.screen.blit(score_bg, (10, 10))
        
        # Score text with glow effect
        score_text = f"Score: {self.score}"
        for offset in [(2, 2), (1, 1), (0, 0)]:
            color = SHADOW if offset != (0, 0) else GOLD if self.score_pulse > 0 else WHITE
            text_surface = score_font.render(score_text, True, color)
            self.screen.blit(text_surface, (15 + offset[0], 20 + offset[1]))
            
        # Removed speed and gap indicators
        
        # Draw start screen
        if not self.game_started and not self.game_over:
            self.draw_start_screen()
            
        # Draw game over screen
        if self.game_over:
            self.draw_game_over_screen()
            
    def draw_start_screen(self):
        # Animated overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 50))
        self.screen.blit(overlay, (0, 0))
        
        # Bouncing title
        bounce_offset = math.sin(self.title_bounce) * 10
        title_y = SCREEN_HEIGHT // 2 - 120 + bounce_offset
        
        self.draw_text_with_shadow("FLAPPY BIRD", self.title_font, GOLD, BLACK,
                                   SCREEN_WIDTH // 2 - 120, int(title_y))
        
        # Subtitle with glow
        subtitle_y = title_y + 60
        self.draw_text_with_shadow("Progressive Difficulty", self.font, WHITE, SHADOW,
                                   SCREEN_WIDTH // 2 - 85, int(subtitle_y))
        
        # Game features
        features = [
            "🚀 Speed increases gradually",
            "📏 Pipe gaps get smaller",
            "🎯 Progressive challenge"
        ]
        
        for i, feature in enumerate(features):
            self.draw_text_with_shadow(feature, self.font, LIGHT_GRAY, BLACK,
                                       SCREEN_WIDTH // 2 - 100, int(subtitle_y) + 30 + i * 25)
        
        # Animated instructions
        pulse = math.sin(pygame.time.get_ticks() * 0.005) * 0.3 + 0.7
        instruction_color = (int(255 * pulse), int(255 * pulse), 255)
        
        self.draw_text_with_shadow("Press SPACE or Click to Start!", self.large_font, instruction_color, BLACK,
                                   SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 80)
        
        # Controls
        self.draw_text_with_shadow("SPACE/Click: Flap Wings", self.font, LIGHT_GRAY, BLACK,
                                   SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120)
        
    def draw_game_over_screen(self):
        # Dramatic overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((50, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text with dramatic effect
        game_over_y = SCREEN_HEIGHT // 2 - 100
        self.draw_text_with_shadow("GAME OVER", self.title_font, RED, BLACK,
                                   SCREEN_WIDTH // 2 - 110, game_over_y)
        
        # Final score with medal effect
        medal_color = GOLD if self.score >= 15 else (192, 192, 192) if self.score >= 8 else (205, 127, 50)
        medal_text = "🏆" if self.score >= 15 else "🥈" if self.score >= 8 else "🥉"
        
        final_score_text = f"Final Score: {self.score} {medal_text}"
        self.draw_text_with_shadow(final_score_text, self.large_font, medal_color, BLACK,
                                   SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 40)
        
        # Final difficulty reached
        # final_speed_text = f"Final Speed: {self.current_speed:.1f}"
        # final_gap_text = f"Final Gap: {int(self.current_gap)}"
        
        # self.draw_text_with_shadow(final_speed_text, self.font, YELLOW, BLACK,
                                #    SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 10)
        # self.draw_text_with_shadow(final_gap_text, self.font, LIGHT_GRAY, BLACK,
                                #    SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 10)
        
        # Performance message
        if self.score >= 20:
            message = "LEGENDARY! 🌟"
            color = GOLD
        elif self.score >= 15:
            message = "AMAZING! ⭐"
            color = YELLOW
        elif self.score >= 10:
            message = "Great Job! 👏"
            color = (0, 255, 0)
        elif self.score >= 5:
            message = "Good Try! 👍"
            color = BLUE
        else:
            message = "Keep Practicing! 💪"
            color = WHITE
            
        self.draw_text_with_shadow(message, self.font, color, BLACK,
                                   SCREEN_WIDTH // 2 - len(message) * 6, SCREEN_HEIGHT // 2 + 40)
        
        # Pulsing restart instructions
        pulse = math.sin(pygame.time.get_ticks() * 0.008) * 0.4 + 0.6
        restart_color = (int(255 * pulse), int(255 * pulse), 255)
        
        self.draw_text_with_shadow("Press R to Restart", self.font, restart_color, BLACK,
                                   SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 70)
        
        self.draw_text_with_shadow("Press Q to Quit", self.font, LIGHT_GRAY, BLACK,
                                   SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 100)
        
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_started:
                        self.game_started = True
                    elif not self.game_over:
                        self.bird.jump()
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_q and self.game_over:
                    return False
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if not self.game_started:
                        self.game_started = True
                    elif not self.game_over:
                        self.bird.jump()
                        
        return True
        
    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
