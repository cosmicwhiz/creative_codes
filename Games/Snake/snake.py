import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WALL_COLOR = WHITE
SNAKE_HEAD_COLOR = (70, 185, 235)  # #ff124f
SNAKE_BODY_COLOR_1 = (255, 0, 160)  # #ff00a0
FOOD_COLOR =  (254, 117, 254) # #120458
MENU_COLOR = (100, 100, 100)
GRID_COLOR = (21, 21, 21)

# Snake and Food
snake = [(400, 400)]
snake_direction = (1, 0)
food = (200, 200)
next_direction = (1, 0)

# Game settings
cell_size = 20
snake_speed = 10 # Adjust the snake's movement speed
last_snake_update_time = pygame.time.get_ticks()
last_food_respawn_time = pygame.time.get_ticks()  # Track the last time food was respawned
food_respawn_interval = 3500  # Food respawn interval in milliseconds (5 seconds)
wall_size = 400
wall_left = (WIDTH - wall_size) // 2
wall_top = (HEIGHT - wall_size) // 2
wall_rect = pygame.Rect(wall_left, wall_top, wall_size, wall_size)

# Scoring
score = 0
max_points_per_food = 20

def is_collision_with_wall(pos):
    x, y = pos
    if not wall_rect.collidepoint(x, y):
        return True
    return False

def is_food_on_snake(pos):
    return pos in snake

def is_self_collision(pos):
    return pos in snake[1:]  # Skip the head while checking for self-collision

def generate_food():
    while True:
        food_pos = (random.randint(wall_left // cell_size, (wall_left + wall_size - cell_size) // cell_size) * cell_size,
                    random.randint(wall_top // cell_size, (wall_top + wall_size - cell_size) // cell_size) * cell_size)
        if not is_food_on_snake(food_pos):
            return food_pos

def calculate_points(elapsed_time):
    # Points are calculated based on the elapsed time and the maximum interval
    # The quicker the snake eats the food, the higher the points earned
    normalized_time = min(elapsed_time, food_respawn_interval) / food_respawn_interval
    points = int(max_points_per_food * (1 - normalized_time))
    return points

def show_game_over_menu():
    menu_width = 300
    menu_height = 150
    menu_left = (WIDTH - menu_width) // 2
    menu_top = (HEIGHT - menu_height) // 2
    menu_rect = pygame.Rect(menu_left, menu_top, menu_width, menu_height)

    pygame.draw.rect(screen, MENU_COLOR, menu_rect)
    pygame.draw.rect(screen, WHITE, menu_rect, 2)

    font = pygame.font.Font(None, 40)
    game_over_text = font.render("Game Over", True, WHITE)
    game_over_text_rect = game_over_text.get_rect(center=(menu_left + menu_width // 2, menu_top + 40))
    screen.blit(game_over_text, game_over_text_rect)

    font = pygame.font.Font(None, 22)
    restart_text = font.render("Hit 'Enter' to restart", True, WHITE)
    restart_text_rect = restart_text.get_rect(center=(menu_left + menu_width // 2, menu_top + 90))
    screen.blit(restart_text, restart_text_rect)

    exit_text = font.render("Hit 'Esc' to exit", True, WHITE)
    exit_text_rect = exit_text.get_rect(center=(menu_left + menu_width // 2, menu_top + 120))
    screen.blit(exit_text, exit_text_rect)

    pygame.display.flip()

# Main game loop
running = True
game_over = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_RETURN:
                # Restart the game
                snake = [(400, 400)]
                snake_direction = (1, 0)
                food = (200, 200)
                next_direction = (1, 0)
                score = 0
                last_snake_update_time = pygame.time.get_ticks()
                last_food_respawn_time = pygame.time.get_ticks()
                game_over = False
            elif game_over and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_UP and snake_direction != (0, 1):
                next_direction = (0, -1)
            elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                next_direction = (0, 1)
            elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                next_direction = (1, 0)

    current_time = pygame.time.get_ticks()
    if not game_over and current_time - last_snake_update_time >= 1000 // snake_speed:
        last_snake_update_time = current_time

        # Update snake position
        new_head = (snake[0][0] + snake_direction[0] * cell_size, snake[0][1] + snake_direction[1] * cell_size)

        # Check self collision
        if is_self_collision(new_head):
            game_over = True

        # Teleport the snake to the opposite side if goes beyond the boundary walls
        if is_collision_with_wall(new_head):
                new_head = (new_head[0] - snake_direction[0] * wall_size , new_head[1] - snake_direction[1] * wall_size)

        if not game_over:
            snake.insert(0, new_head)

            # Update the snake's direction if the intended direction is not opposite
            if snake_direction != (-next_direction[0], -next_direction[1]):
                snake_direction = next_direction

            # Check collision with food
            if new_head == food:
                elapsed_time = current_time - last_food_respawn_time
                points = calculate_points(elapsed_time)
                score += points
                food = generate_food()
                last_food_respawn_time = current_time  # Reset the timer
            else:
                snake.pop()

            # Respawn the food every 5 seconds
            if current_time - last_food_respawn_time >= food_respawn_interval:
                food = generate_food()
                last_food_respawn_time = current_time
            
    # Draw
    screen.fill(BLACK)

    # Draw light color grid lines on the play area
    for x in range(wall_left + cell_size, wall_left + wall_size, cell_size):
        pygame.draw.line(screen, GRID_COLOR, (x, wall_top), (x, wall_top + wall_size))
    for y in range(wall_top + cell_size, wall_top + wall_size, cell_size):
        pygame.draw.line(screen, GRID_COLOR, (wall_left, y), (wall_left + wall_size, y))

    for i, segment in enumerate(snake):
        # Determine the color based on head or body segment
        if i == 0:
            color = SNAKE_HEAD_COLOR
        else:
            color = SNAKE_BODY_COLOR_1
        pygame.draw.rect(screen, color, (*segment, cell_size, cell_size), 1)
    pygame.draw.rect(screen, FOOD_COLOR, (*food, cell_size, cell_size))

    # Draw the wall
    pygame.draw.rect(screen, WALL_COLOR, wall_rect, 1)

    # Draw the score box above the wall
    pygame.draw.rect(screen, WALL_COLOR, (wall_left, wall_top - 40, wall_size, 41))
    font = pygame.font.Font(None, 30)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (wall_left + 10, wall_top - 30))

    if game_over:
        show_game_over_menu()

    pygame.display.flip()
    clock.tick(60)
