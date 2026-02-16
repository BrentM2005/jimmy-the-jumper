import pygame
import sys
import json
import os
import pygame.mixer
from src.config import *
from src.player import Player
from src.level_manager import LevelManager
from src.camera import Camera

SAVE_FILE = "save.json"

class Game:
    def __init__(self):
        pygame.init()
        self.audio_available = True
        try:
            pygame.mixer.init()
        except pygame.error:
            self.audio_available = False

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)

        if self.audio_available:
            self.jump_sound = pygame.mixer.Sound(pygame.mixer.Sound(buffer=b'\x00\x7f' * 1000))
            self.coin_sound = pygame.mixer.Sound(pygame.mixer.Sound(buffer=b'\x7f\x00' * 1000))
            self.death_sound = pygame.mixer.Sound(pygame.mixer.Sound(buffer=b'\x00\x00' * 500 + b'\x7f' * 500))
        else:
            self.jump_sound = None
            self.coin_sound = None
            self.death_sound = None

        pygame.joystick.init()
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Controller detected: {self.joystick.get_name()}")

        self.state = "MENU"
        self.level_manager = LevelManager()
        self.camera = None
        self.player = None
        self.high_score = 0
        self.start_background_music()

    def start_background_music(self):
        if not self.audio_available:
            return
        try:
            pygame.mixer.music.load("assets/sounds/background.mp3")
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
        except (pygame.error, FileNotFoundError):
            pass

    def init_game(self):
        self.level_manager.reset_to_first_level()
        self.camera = Camera(self.level_manager.level.world_width, SCREEN_HEIGHT)
        self.player = Player(
            self.level_manager.level.spawn_x,
            self.level_manager.level.spawn_y,
            self.joystick
        )

    def save_game(self):
        """Save current game state to a JSON file."""
        if self.player is None:
            return
        data = {
            "level_index": self.level_manager.current_level,
            "score": self.player.score,
            "lives": self.player.lives,
            "high_score": self.high_score
        }
        try:
            with open(SAVE_FILE, "w") as f:
                json.dump(data, f)
            print("Game saved.")
        except Exception as e:
            print(f"Save failed: {e}")

    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            return False
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
            self.level_manager.current_level = data["level_index"]
            self.level_manager.load_current_level()
            self.camera = Camera(self.level_manager.level.world_width, SCREEN_HEIGHT)
            self.player = Player(
                self.level_manager.level.spawn_x,
                self.level_manager.level.spawn_y,
                self.joystick
            )
            self.player.score = data["score"]
            self.player.lives = data["lives"]
            self.high_score = data["high_score"]
            self.state = "PLAYING"
            return True
        except Exception as e:
            print(f"Load failed: {e}")
            return False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.JOYAXISMOTION:
                if self.player and event.axis == 0:  
                    self.player.joy_axis_x = event.value

            if event.type == pygame.JOYBUTTONDOWN:
                if self.player and event.button == 0:  
                    self.player.jump()
                    if self.jump_sound:
                        self.jump_sound.play()

            if event.type == pygame.KEYDOWN:
                if self.state == "MENU":
                    if event.key == pygame.K_RETURN:
                        self.init_game()
                        self.state = "PLAYING"
                    elif event.key == pygame.K_i:
                        self.state = "INSTRUCTIONS"
                    elif event.key == pygame.K_l:
                        if self.load_game():
                            print("Loaded successfully.")
                        else:
                            print("No save file found.")
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                elif self.state == "INSTRUCTIONS":
                    self.state = "MENU"

                elif self.state == "PLAYING":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                        self.player.jump()
                        if self.jump_sound:
                            self.jump_sound.play()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "PAUSED"
                    elif event.key == pygame.K_F5:
                        self.save_game()

                elif self.state in ["PAUSED", "GAME_OVER", "WIN"]:
                    if event.key == pygame.K_RETURN:
                        if self.state == "PAUSED":
                            self.state = "PLAYING"
                        else:
                            self.init_game()
                            self.state = "PLAYING"
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "MENU"

    def update(self, dt):
        if self.state == "PLAYING":
            self.level_manager.level.update(self.player, dt)
            self.player.update(self.level_manager.level.platforms)
            if self.player.rect.left < 0:
                self.player.rect.left = 0
                self.player.vel_x = 0
            self.camera.update(self.player)

            pow_hits = pygame.sprite.spritecollide(self.player, self.level_manager.level.powerups, True)
            for p in pow_hits:
                self.player.activate_powerup(p.type)
                self.player.score += 50
                if self.coin_sound:
                    self.coin_sound.play()

            coin_hits = pygame.sprite.spritecollide(self.player, self.level_manager.level.coins, True)
            for _ in coin_hits:
                self.player.score += 10
                if self.coin_sound:
                    self.coin_sound.play()

            spike_hits = pygame.sprite.spritecollide(self.player, self.level_manager.level.spikes, False)
            for _ in spike_hits:
                if not self.player.invincible:
                    self.player.lives -= 1
                    if self.death_sound:
                        self.death_sound.play()
                    if self.player.lives <= 0:
                        self.state = "GAME_OVER"
                        if self.player.score > self.high_score:
                            self.high_score = self.player.score
                    else:
                        self.player.respawn(self.level_manager.level.spawn_x, self.level_manager.level.spawn_y)
                break

            if pygame.sprite.spritecollide(self.player, self.level_manager.level.goals, False):
                next_lev = self.level_manager.next_level()
                if next_lev is None:
                    self.state = "WIN"
                else:
                    self.camera = Camera(next_lev.world_width, SCREEN_HEIGHT)
                    self.player.respawn(next_lev.spawn_x, next_lev.spawn_y)
                return

            enemy_hits = pygame.sprite.spritecollide(self.player, self.level_manager.level.enemies, False)
            for enemy in enemy_hits:
                if self.player.vel_y > 0 and self.player.rect.bottom < enemy.rect.centery:
                    enemy.kill()
                    self.player.score += 50
                    self.player.vel_y = JUMP_POWER * 0.7
                    if self.coin_sound:
                        self.coin_sound.play()
                else:
                    if not self.player.invincible:
                        self.player.lives -= 1
                        if self.death_sound:
                            self.death_sound.play()
                        if self.player.lives <= 0:
                            self.state = "GAME_OVER"
                            if self.player.score > self.high_score:
                                self.high_score = self.player.score
                        else:
                            self.player.respawn(self.level_manager.level.spawn_x, self.level_manager.level.spawn_y)
                break

            if self.level_manager.level.time_remaining <= 0 and not self.player.invincible:
                self.player.lives -= 1
                if self.death_sound:
                    self.death_sound.play()
                if self.player.lives <= 0:
                    self.state = "GAME_OVER"
                    if self.player.score > self.high_score:
                        self.high_score = self.player.score
                else:
                    self.player.respawn(self.level_manager.level.spawn_x, self.level_manager.level.spawn_y)

            if self.player.rect.top > SCREEN_HEIGHT * 2 and not self.player.invincible:
                self.player.lives -= 1
                if self.death_sound:
                    self.death_sound.play()
                if self.player.lives <= 0:
                    self.state = "GAME_OVER"
                    if self.player.score > self.high_score:
                        self.high_score = self.player.score
                else:
                    self.player.respawn(self.level_manager.level.spawn_x, self.level_manager.level.spawn_y)
                return

    def draw_text(self, text, font, color, x, y, center=False):
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surface, rect)

    def draw(self):
        self.screen.fill(SKY_BLUE)

        if self.state == "MENU":
            self.draw_text("JIMMY THE JUMPER", self.big_font, BLUE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, center=True)
            self.draw_text("ENTER: Start | I: Instructions | L: Load Game | ESC: Quit", self.font, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)

        elif self.state == "INSTRUCTIONS":
            self.draw_text("INSTRUCTIONS", self.big_font, BLUE, SCREEN_WIDTH // 2, 100, center=True)
            inst = [
                "A/D or Arrows: Move",
                "W/Space: Jump",
                "ESC: Pause/Menu",
                "F5: Save Game",
                "Collect coins (+10 pts)",
                "Jump on enemies (+50 pts)",
                "Reach goal to win level",
                "3 Lives - Don't fall!"
            ]
            for i, line in enumerate(inst):
                self.draw_text(line, self.font, BLACK, 50, 200 + i * 40)

        elif self.state == "PAUSED":
            self.level_manager.level.draw(self.screen, self.camera)
            self.screen.blit(self.player.image, self.camera.apply(self.player))
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            self.draw_text("PAUSED", self.big_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
            self.draw_text("ENTER: Resume | ESC: Menu", self.font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, center=True)

        elif self.state == "PLAYING":
            self.level_manager.level.draw(self.screen, self.camera)
            self.screen.blit(self.player.image, self.camera.apply(self.player))

            self.draw_text(f"Lives: {self.player.lives}", self.font, BLACK, 10, 10)
            self.draw_text(f"Score: {self.player.score}", self.font, BLACK, 10, 40)
            self.draw_text(f"Level: {self.level_manager.get_current_level_id()}", self.font, BLACK, 10, 70)
            self.draw_text(f"High: {self.high_score}", self.font, BLACK, SCREEN_WIDTH - 150, 10)
            self.draw_text(f"Time: {int(self.level_manager.level.time_remaining)}", self.font, BLACK, SCREEN_WIDTH - 150, 40)

        elif self.state == "GAME_OVER":
            self.screen.fill(BLACK)
            self.draw_text("GAME OVER", self.big_font, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, center=True)
            self.draw_text(f"Final: {self.player.score}", self.font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
            self.draw_text(f"High: {self.high_score}", self.font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30, center=True)
            self.draw_text("ENTER: Restart | ESC: Menu", self.font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90, center=True)

        elif self.state == "WIN":
            self.screen.fill(WHITE)
            self.draw_text("YOU WON ALL LEVELS!", self.big_font, GREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, center=True)
            self.draw_text(f"Final: {self.player.score}", self.font, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
            self.draw_text(f"High: {self.high_score}", self.font, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30, center=True)
            self.draw_text("ENTER: Play Again | ESC: Menu", self.font, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90, center=True)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            dt = self.clock.get_time() / 1000.0
            self.update(dt)
            self.draw()
            self.clock.tick(FPS)