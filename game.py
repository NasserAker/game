import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Flappy Bird Clone")

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)

# Game settings
bird_width, bird_height = 40, 30
bird_x = WIDTH // 6
bird_base_speed = 6  # Faster initial movement
gravity = 0.5

# Pipe settings
pipe_width = 70
initial_pipe_gap = 130  # Initial gap
initial_pipe_speed = 4
initial_pipe_frequency = 1500  # Milliseconds

# Initialize font
font = pygame.font.Font(None, 36)

# Game variables
clock = pygame.time.Clock()
score = 0
pipes = []
last_pipe = pygame.time.get_ticks()
game_speed_multiplier = 1.0

# Function to create a new set of pipes
def create_pipe(pipe_gap):
    pipe_height = random.randint(50, HEIGHT - pipe_gap - 50)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, pipe_height)
    bottom_pipe = pygame.Rect(WIDTH, pipe_height + pipe_gap, pipe_width, HEIGHT - pipe_height - pipe_gap)
    return top_pipe, bottom_pipe

# Function to display "Game Over" and prompt to play again
def game_over_screen():
    screen.fill(WHITE)
    game_over_text = font.render("Game Over! Press SPACE to Play Again or ESC to Quit", True, BLACK)
    score_text = font.render(f"Your Score: {int(score)}", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True  # Restart game
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clock.tick(15)

# Function to reset all game variables for a new game
def reset_game():
    global bird_y, bird_velocity_y, score, pipes, last_pipe, game_speed_multiplier, pipe_speed, pipe_gap, pipe_frequency
    bird_y = HEIGHT // 2
    bird_velocity_y = 0
    score = 0
    pipes.clear()
    last_pipe = pygame.time.get_ticks()
    game_speed_multiplier = 1.0
    pipe_speed = initial_pipe_speed
    pipe_gap = initial_pipe_gap
    pipe_frequency = initial_pipe_frequency

# Main game loop
running = True
while running:
    reset_game()  # Reset game variables at the start of each game

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    bird_velocity_y = -bird_base_speed * game_speed_multiplier
                elif event.key == pygame.K_DOWN:
                    bird_velocity_y = bird_base_speed * game_speed_multiplier
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    bird_velocity_y = 0

        # Bird mechanics
        bird_y += bird_velocity_y
        bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)

        # Generate pipes at intervals
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe > pipe_frequency:
            pipes.extend(create_pipe(pipe_gap))
            last_pipe = current_time

        # Move pipes and detect collisions
        pipes = [pipe.move(-int(pipe_speed * game_speed_multiplier), 0) for pipe in pipes if pipe.x > -pipe_width]
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                if game_over_screen():
                    reset_game()
                    break
                else:
                    running = False
                    pygame.quit()
                    sys.exit()

        # Check if bird is out of bounds
        if bird_rect.top < 0 or bird_rect.bottom > HEIGHT:
            if game_over_screen():
                reset_game()
                break
            else:
                running = False
                pygame.quit()
                sys.exit()

        # Draw bird
        pygame.draw.rect(screen, BLACK, bird_rect)

        # Draw pipes
        for pipe in pipes:
            pygame.draw.rect(screen, GREEN, pipe)

        # Update score and adjust difficulty
        for pipe in pipes:
            if pipe.right < bird_x and not pipe.width == 0:
                score += 0.5  # Each set of pipes passed counts as 1
                pipe.width = 0  # Mark pipe as "scored"
                game_speed_multiplier += 0.03  # Increase game speed by 3%
                pipe_frequency = max(800, pipe_frequency * 0.97)  # Decrease pipe spacing
                pipe_gap = max(100, int(initial_pipe_gap / game_speed_multiplier))  # Decrease gap size

        # Display score
        score_text = font.render(f"Score: {int(score)}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

pygame.quit()
