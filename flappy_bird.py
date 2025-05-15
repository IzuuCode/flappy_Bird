import pygame
import random
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 32)

# Game variables
gravity = 0.5
bird_movement = 0
score = 0
high_score = 0
game_active = False

# Load images
bg_surface = pygame.image.load("assets/background.png").convert()
bg_surface = pygame.transform.scale(bg_surface, (WIDTH, HEIGHT))

bird_surface = pygame.image.load("assets/bird.png").convert_alpha()
bird_surface = pygame.transform.scale(bird_surface, (40, 30))
bird_rect = bird_surface.get_rect(center=(100, HEIGHT // 2))

pipe_surface = pygame.image.load("assets/pipe.png").convert()
pipe_surface = pygame.transform.scale(pipe_surface, (60, 400))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

base_surface = pygame.image.load("assets/base.png").convert()
base_surface = pygame.transform.scale(base_surface, (WIDTH, 100))
base_y = HEIGHT - 100

# Load sounds
flap_sound = pygame.mixer.Sound("assets/jump.wav")
hit_sound = pygame.mixer.Sound("assets/hit.wav")

# Functions
def create_pipe():
    pipe_height = random.randint(150, 400)
    bottom_pipe = pipe_surface.get_rect(midtop=(WIDTH + 60, pipe_height))
    top_pipe = pipe_surface.get_rect(midbottom=(WIDTH + 60, pipe_height - 150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 4
    return [pipe for pipe in pipes if pipe.right > -50]

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT:
            SCREEN.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            SCREEN.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= base_y:
        hit_sound.play()
        return False
    return True

def draw_base():
    SCREEN.blit(base_surface, (0, base_y))

def show_score(state):
    if state == "main":
        score_surface = FONT.render(f"Score: {int(score)}", True, (255, 255, 255))
        SCREEN.blit(score_surface, (10, 10))
    elif state == "game_over":
        score_surface = FONT.render(f"Score: {int(score)}", True, (255, 255, 255))
        high_score_surface = FONT.render(f"High Score: {int(high_score)}", True, (255, 255, 255))
        SCREEN.blit(score_surface, (WIDTH//2 - 80, HEIGHT//2 - 50))
        SCREEN.blit(high_score_surface, (WIDTH//2 - 110, HEIGHT//2))

def show_start_menu():
    title = FONT.render("Flappy Bird", True, (255, 255, 0))
    start_msg = FONT.render("Press SPACE to Start", True, (255, 255, 255))
    SCREEN.blit(title, (WIDTH//2 - 90, HEIGHT//2 - 100))
    SCREEN.blit(start_msg, (WIDTH//2 - 130, HEIGHT//2 - 40))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird_movement = 0
                    bird_movement -= 10
                    flap_sound.play()
                else:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (100, HEIGHT // 2)
                    bird_movement = 0
                    score = 0

        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())

    SCREEN.blit(bg_surface, (0, 0))

    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        SCREEN.blit(bird_surface, bird_rect)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        game_active = check_collision(pipe_list)

        for pipe in pipe_list:
            if pipe.centerx == bird_rect.centerx:
                score += 0.5
        show_score("main")
    else:
        if score > high_score:
            high_score = score
        show_start_menu() if score == 0 else show_score("game_over")
        SCREEN.blit(bird_surface, bird_rect)

    draw_base()
    pygame.display.update()
    CLOCK.tick(60)
