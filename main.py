import os
import pygame
import random
import math
from pygame import mixer
import time
from finger_tracking import FingerTracker

# game constants
WIDTH = 800
HEIGHT = 600

# global variables
running = True
pause_state = 0
score = 0
life = 3  # Player life starts at 3
boss_life = 15  # Boss health (hits to kill)
boss_spawned = False  # Boss will only appear after 1000 points
kills = 0
initial_player_velocity = 3.0
initial_enemy_velocity = 1.0
weapon_shot_velocity = 5.0
enemy_bullet_speed = 5.0
max_enemies = 6
enemy_spawn_timer = 0  # Timer for controlling enemy spawn intervals
game_over = False

# initialize pygame
pygame.init()

# Input key states (keyboard)
LEFT_ARROW_KEY_PRESSED = 0
RIGHT_ARROW_KEY_PRESSED = 0
SPACE_BAR_PRESSED = 0
ESC_KEY_PRESSED = 0

# create display window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nebula Assault")

# File paths
def get_resource_path(file_name):
    base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "res", file_name)

window_icon = pygame.image.load(get_resource_path("images/alien.png"))
pygame.display.set_icon(window_icon)

# game sounds
enemy_explosion_sound = mixer.Sound(get_resource_path("sounds/explosion.wav"))
bullet_fire_sound = mixer.Sound(get_resource_path("sounds/gunshot.wav"))
player_hit_sound = mixer.Sound(get_resource_path("sounds/player_hit.wav"))
boss_hit_sound = mixer.Sound(get_resource_path("sounds/boss_hit.wav"))
game_over_sound = mixer.Sound(get_resource_path("sounds/gameover.wav"))

# create background
background_img = pygame.image.load(get_resource_path("images/background.png"))  # 800 x 600 px image

# Font for displaying score
font = pygame.font.Font('freesansbold.ttf', 32)

def display_score():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(score_text, (10, 10))

def display_life():
    life_text = font.render(f"Lives: {life}", True, (255, 255, 255))
    window.blit(life_text, (10, 50))

def display_boss_life():
    if boss_life > 0:
        boss_life_text = font.render(f"Boss HP: {boss_life}", True, (255, 0, 0))
        window.blit(boss_life_text, (WIDTH - 200, 10))

# create player class
class Player:
    def __init__(self, img_path, width, height, x, y, dx, dy):
        self.img = pygame.image.load(img_path)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def draw(self):
        window.blit(self.img, (self.x, self.y))

# create bullet class
class Bullet:
    def __init__(self, img_path, width, height, x, y, dx, dy, fired=False):
        self.img = pygame.image.load(img_path)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.fired = fired

    def draw(self):
        if self.fired:
            window.blit(self.img, (self.x, self.y))
            self.y -= self.dy

        # Reset bullet when it goes off the screen
        if self.y < 0 or self.y > HEIGHT:  # Add condition to reset if it goes off the screen
            self.fired = False

# create enemy class
class Enemy:
    def __init__(self, img_path, width, height, x, y, dx, dy):
        self.img = pygame.image.load(img_path)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.bullet = Bullet(get_resource_path("images/beam.png"), 16, 16, self.x, self.y, 0, -enemy_bullet_speed)  # Adjusted speed to make bullets go down

    def move(self):
        self.x += self.dx
        if self.x <= 0 or self.x >= WIDTH - self.width:
            self.dx *= -1
            self.y += self.dy

    def shoot(self):
        if not self.bullet.fired:
            self.bullet.fired = True
            self.bullet.x = self.x + self.width // 2
            self.bullet.y = self.y + self.height // 2

    def draw(self):
        window.blit(self.img, (self.x, self.y))
        self.bullet.draw()

# create boss class with erratic movement
class Boss:
    def __init__(self, img_path, width, height, x, y):
        self.img = pygame.image.load(img_path)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.dx = random.choice([-3, -2, -1, 1, 2, 3])  # Random horizontal speed
        self.dy = random.choice([-2, -1, 1, 2])  # Random vertical speed
        self.homing_bullet = Bullet(get_resource_path("images/boss_bullet.png"), 24, 24, self.x, self.y, 0, 0, False)

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Reverse direction when hitting screen edges
        if self.x <= 0 or self.x >= WIDTH - self.width:
            self.dx *= -1
        if self.y <= 0 or self.y >= HEIGHT // 2:  # Boss stays in the upper half
            self.dy *= -1

    def draw(self):
        window.blit(self.img, (self.x, self.y))

    def shoot_homing_bullet(self, player_x, player_y):
        if not self.homing_bullet.fired:
            self.homing_bullet.fired = True
            self.homing_bullet.x = self.x + self.width // 2
            self.homing_bullet.y = self.y + self.height // 2

        # Homing bullet follows the player
        direction_x = player_x - self.homing_bullet.x
        direction_y = player_y - self.homing_bullet.y
        distance = math.sqrt(direction_x**2 + direction_y**2)

        if distance > 0:
            self.homing_bullet.dx = (direction_x / distance) * 2  # Adjust speed
            self.homing_bullet.dy = (direction_y / distance) * 2
        self.homing_bullet.x += self.homing_bullet.dx
        self.homing_bullet.y += self.homing_bullet.dy

    def draw_bullet(self):
        self.homing_bullet.draw()

# Collision detection
def is_collision(obj1, obj2):
    distance = math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)
    return distance < (obj1.width / 2 + obj2.width / 2)

# Initialize the game objects
def init_game():
    global player, bullet, enemies, boss, enemy_spawn_timer

    # Initialize Player
    player = Player(get_resource_path("images/spaceship.png"), 64, 64, WIDTH // 2, HEIGHT - 100, initial_player_velocity, 0)

    # Initialize Bullet
    bullet = Bullet(get_resource_path("images/laser.png"), 32, 32, 0, 0, 0, weapon_shot_velocity)

    # Initialize Enemies
    enemies = [Enemy(get_resource_path("images/enemy.png"), 64, 64, random.randint(0, WIDTH - 64), random.randint(50, 150), initial_enemy_velocity, 40)]  # Start with 1 enemy
    enemy_spawn_timer = time.time()  # Start enemy spawn timer

    # Initialize Boss (but don't spawn it yet)
    boss = Boss(get_resource_path("images/boss.png"), 128, 128, WIDTH // 2 - 64, 50)
    