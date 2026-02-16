import pygame
from src.config import *
from src.assets import AssetLoader

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, joystick=None):
        super().__init__()
        
        self.img_idle = AssetLoader.load_image("Characters/player_idle.png", 32, 32, BLUE)
        self.img_run = AssetLoader.load_image("Characters/player_run.png", 32, 32, BLUE)
        self.img_jump = AssetLoader.load_image("Characters/player_jump.png", 32, 32, BLUE)
        self.image = self.img_idle
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_y = 0
        self.vel_x = 0
        self.on_ground = False
        self.on_platform = None
        self.lives = 3  
        self.score = 0
        self.can_double_jump = False
        self.has_double_jumped = False
        self.facing_right = True
        self.invincible = False
        self.invincibility_timer = 0.0
        self.speed_multiplier = 1.0
        self.speed_boost_timer = 0.0
        self.joystick = joystick
        self.joy_axis_x = 0.0          
        self.deadzone = 0.2

    def update(self, platforms):
        dt = 1/60.0
        if self.invincibility_timer > 0:
            self.invincibility_timer -= dt
            if self.invincibility_timer <= 0:
                self.invincible = False
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= dt
            if self.speed_boost_timer <= 0:
                self.speed_multiplier = 1.0

        self.handle_input()
        self.apply_friction()
        self.rect.x += self.vel_x
        self.check_horizontal_collisions(platforms)
        self.apply_gravity()
        self.rect.y += self.vel_y
        self.check_vertical_collisions(platforms)
        
        if self.on_platform is not None and self.rect.colliderect(self.on_platform.rect):
            self.rect.x += self.on_platform.vel_x
        else:
            self.on_platform = None
            
        self.animate()

    def animate(self):
        if not self.on_ground:
            self.image = self.img_jump
        elif abs(self.vel_x) > 0.5:
            if (pygame.time.get_ticks() // 150) % 2 == 0:
                self.image = self.img_idle
            else:
                self.image = self.img_run
        else:
            self.image = self.img_idle
        
        if self.vel_x < 0:
            self.facing_right = True
        elif self.vel_x > 0:
            self.facing_right = False
            
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
        
        if self.invincible and (pygame.time.get_ticks() // 120) % 2 == 0:
            self.image.set_alpha(120)
        else:
            self.image.set_alpha(255)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED * self.speed_multiplier
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED * self.speed_multiplier

        if self.joystick:
            axis = self.joy_axis_x
            if abs(axis) > self.deadzone:
                joy_speed = axis * PLAYER_SPEED * self.speed_multiplier
                self.vel_x += joy_speed

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_POWER
            self.on_ground = False
            self.has_double_jumped = False
        elif self.can_double_jump and not self.has_double_jumped:
            self.vel_y = JUMP_POWER * 0.85
            self.has_double_jumped = True

    def activate_powerup(self, p_type):
        if p_type == "double_jump":
            self.can_double_jump = True
        elif p_type == "invincibility":
            self.invincibility_timer = 5.0
            self.invincible = True
        elif p_type == "speed_boost":
            self.speed_boost_timer = 10.0
            self.speed_multiplier = 2.0

    def apply_gravity(self):
        self.vel_y += GRAVITY

    def apply_friction(self):
        self.vel_x += FRICTION * self.vel_x
        if abs(self.vel_x) < 0.1:
            self.vel_x = 0

    def check_horizontal_collisions(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hits:
            if self.vel_x > 0:
                self.rect.right = hit.rect.left
                self.vel_x = 0
            elif self.vel_x < 0:
                self.rect.left = hit.rect.right
                self.vel_x = 0

    def check_vertical_collisions(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.on_ground = False
        for hit in hits:
            if self.vel_y > 0:
                self.rect.bottom = hit.rect.top
                self.vel_y = 0
                self.on_ground = True
                self.on_platform = hit
                self.has_double_jumped = False
            elif self.vel_y < 0:
                self.rect.top = hit.rect.bottom
                self.vel_y = 0

    def respawn(self, spawn_x, spawn_y):
        self.rect.topleft = (spawn_x, spawn_y)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.on_platform = None
        self.invincible = False
        self.invincibility_timer = 0.0
        self.speed_multiplier = 1.0
        self.speed_boost_timer = 0.0
        self.joy_axis_x = 0.0