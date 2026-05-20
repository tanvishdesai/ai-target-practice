import pygame
import random
# Custom event type for targets escaping
TARGET_ESCAPED_EVENT = pygame.USEREVENT + 1
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load only 3 explosion frames
        self.images = [
            pygame.image.load(f"assets/explosion/explosion_{i}.png").convert_alpha()
            for i in range(1, 4)  # Now uses explosion_1.png, explosion_2.png, explosion_3.png
        ]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 3  # Slower animation to compensate for fewer frames
        self.frame_counter = 0

    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.index += 1
            if self.index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.index]
                self.frame_counter = 0  # Reset counter

class Target(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, offset_x=0):
        super().__init__()
        self.image = pygame.image.load("assets/targets/pizza.png").convert_alpha()
        self.rect = self.image.get_rect()
        # Center targets horizontally with offset
        self.rect.x = (screen_width // 2 - self.rect.width // 2) + offset_x
        self.rect.y = -self.rect.height
        self.speed = random.randint(3, 5)
        self.is_hit = False

    def update(self):
        if not self.is_hit:
            self.rect.y += self.speed
            if self.rect.y > 600:
                self.kill()
                pygame.event.post(pygame.event.Event(TARGET_ESCAPED_EVENT))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((10, 20), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (255, 0, 0), [(0, 0), (10, 0), (5, 20)])
        
        # Rotate bullet to face direction (use -angle for Pygame's rotation)
        self.image = pygame.transform.rotate(self.image, -angle)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Calculate velocity (rotate Vector2 by -angle)
        self.speed = 15
        direction = pygame.math.Vector2(1, 0).rotate(-angle)  # Fix: Negative angle
        self.velocity = direction * self.speed

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if self.rect.y < -20 or self.rect.x < 0 or self.rect.x > 800:
            self.kill()

class Game:
    def __init__(self, screen_width=800, screen_height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.all_targets = pygame.sprite.Group()
        self.all_bullets = pygame.sprite.Group()
        self.all_explosions = pygame.sprite.Group()
        self.score = 0
        self.lives = 3
        self.ammo = 10  # Initialize ammo
        self.game_over = False
        self.last_hit_time = pygame.time.get_ticks()
        
        # Load assets
        self.heart_image = pygame.image.load("assets/hearts/heart.png").convert_alpha()
        self.shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.wav")
        self.explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")

    def spawn_target(self, offset_x=0):
        new_target = Target(self.screen.get_width(), self.screen.get_height(), offset_x)
        self.all_targets.add(new_target)

    def draw_lives(self):
        for i in range(self.lives):
            self.screen.blit(self.heart_image, (10 + i * 40, 50))

    def draw_ammo(self):  # NEW METHOD: Draw ammo counter
        font = pygame.font.Font(None, 36)
        ammo_text = font.render(f"Ammo: {self.ammo}", True, (255, 255, 255))
        self.screen.blit(ammo_text, (10, 80))  # Position below score

    def draw_game_over(self):
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(text, (250, 250))
        text = font.render("Press R to restart", True, (255, 255, 255))
        self.screen.blit(text, (200, 350))
    def __init__(self, screen_width=800, screen_height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.all_targets = pygame.sprite.Group()
        self.all_bullets = pygame.sprite.Group()
        self.all_explosions = pygame.sprite.Group()
        self.score = 0
        self.lives = 3
        self.game_over = False
        
        # Initialize timing variables
        self.last_hit_time = pygame.time.get_ticks()  # Add this line
        
        # Load assets
        self.heart_image = pygame.image.load("assets/hearts/heart.png").convert_alpha()
        self.shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.wav")
        self.explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
        self.ammo = 25  # Start with 10 bullets
        self.last_hit_time = pygame.time.get_ticks()

    def spawn_target(self):
        new_target = Target(self.screen.get_width(), self.screen.get_height())
        self.all_targets.add(new_target)

    def draw_lives(self):
        for i in range(self.lives):
            self.screen.blit(self.heart_image, (10 + i * 40, 50))

    def draw_game_over(self):
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(text, (250, 250))
        text = font.render("Press R to restart", True, (255, 255, 255))
        self.screen.blit(text, (200, 350))
        running = True
        while running:
            self.clock.tick(30)
            self.screen.fill((0, 0, 0))  # Black background
            
            # Game logic here (called from main.py)
            self.all_targets.update()
            self.all_bullets.update()
            
            # Detect collisions
            for bullet in self.all_bullets:
                hits = pygame.sprite.spritecollide(bullet, self.all_targets, True)
                for _ in hits:
                    self.score += 100
                    self.explosion_sound.play()
            
            # Draw sprites
            self.all_targets.draw(self.screen)
            self.all_bullets.draw(self.screen)
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()