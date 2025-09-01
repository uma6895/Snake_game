import pygame
import random
import sys
from enum import Enum
from typing import List, Tuple
import pygame
# Initialize pygame

pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 200, 0)

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.positions = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = Direction.RIGHT
        self.grow = False

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction.value
        new_x = (head_x + dir_x) % GRID_COUNT
        new_y = (head_y + dir_y) % GRID_COUNT
        
        # Check for self collision
        if (new_x, new_y) in self.positions[1:]:
            return False
            
        self.positions.insert(0, (new_x, new_y))
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
        return True

    def reset(self):
        self.positions = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = Direction.RIGHT
        self.grow = False

    def render(self, surface):
        for i, pos in enumerate(self.positions):
            color = DARK_GREEN if i == 0 else GREEN
            rect = pygame.Rect(
                pos[0] * GRID_SIZE, 
                pos[1] * GRID_SIZE, 
                GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 30)
        self.reset_game()

    def reset_game(self):
        self.snake = Snake()
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False

    def spawn_food(self):
        while True:
            food_pos = (
                random.randint(0, GRID_COUNT - 1),
                random.randint(0, GRID_COUNT - 1)
            )
            if food_pos not in self.snake.positions:
                return food_pos

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != Direction.DOWN:
                    self.snake.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.snake.direction != Direction.UP:
                    self.snake.direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and self.snake.direction != Direction.RIGHT:
                    self.snake.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.snake.direction != Direction.LEFT:
                    self.snake.direction = Direction.RIGHT
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
        return True

    def update(self):
        if self.game_over:
            return
            
        if not self.snake.update():
            self.game_over = True
            return
            
        # Check if snake ate food
        if self.snake.get_head_position() == self.food:
            self.snake.grow = True
            self.food = self.spawn_food()
            self.score += 1

    def render(self):
        self.screen.fill(BLACK)
        
        # Draw grid
        for x in range(0, WINDOW_SIZE, GRID_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, WINDOW_SIZE))
            pygame.draw.line(self.screen, (40, 40, 40), (0, x), (WINDOW_SIZE, x))
        
        # Draw food
        food_rect = pygame.Rect(
            self.food[0] * GRID_SIZE, 
            self.food[1] * GRID_SIZE, 
            GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(self.screen, RED, food_rect)
        
        # Draw snake
        self.snake.render(self.screen)
        
        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        if self.game_over:
            self.render_game_over()
            
        pygame.display.flip()
    
    def render_game_over(self):
        overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render('GAME OVER', True, WHITE)
        score_text = self.font.render(f'Final Score: {self.score}', True, WHITE)
        restart_text = self.font.render('Press R to Restart', True, WHITE)
        
        self.screen.blit(game_over_text, 
                         (WINDOW_SIZE//2 - game_over_text.get_width()//2, 
                          WINDOW_SIZE//2 - 60))
        self.screen.blit(score_text, 
                        (WINDOW_SIZE//2 - score_text.get_width()//2, 
                         WINDOW_SIZE//2))
        self.screen.blit(restart_text, 
                        (WINDOW_SIZE//2 - restart_text.get_width()//2, 
                         WINDOW_SIZE//2 + 60))

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
