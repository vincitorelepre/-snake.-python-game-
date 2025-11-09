import pygame
import random
import sys
import os
from pygame.locals import *

# Инициализация pygame
pygame.init()

# Константы
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
FPS = 10

# Цвета
BACKGROUND_COLOR = (0, 0, 0)
GRID_COLOR = (40, 40, 40)
SNAKE_COLOR = (0, 255, 0)
SNAKE_HEAD_COLOR = (0, 200, 0)
FOOD_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)
GAME_OVER_COLOR = (255, 50, 50)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.grow_to = 3
        
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
    
    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        # Проверка на столкновение с собой
        if new_position in self.positions[1:]:
            return False
        
        self.positions.insert(0, new_position)
        
        if len(self.positions) > self.grow_to:
            self.positions.pop()
            
        return True
    
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            if i == 0:  # Голова змейки
                pygame.draw.rect(surface, SNAKE_HEAD_COLOR, rect)
                pygame.draw.rect(surface, (0, 100, 0), rect, 1)
            else:  # Тело змейки
                pygame.draw.rect(surface, SNAKE_COLOR, rect)
                pygame.draw.rect(surface, (0, 150, 0), rect, 1)
    
    def grow(self):
        self.grow_to += 1
        self.score += 10

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), 
                         random.randint(0, GRID_HEIGHT - 1))
    
    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), 
                          (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, FOOD_COLOR, rect)
        pygame.draw.rect(surface, (150, 0, 0), rect, 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Змейка')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 24)
        self.big_font = pygame.font.SysFont('arial', 48)
        self.snake = Snake()
        self.food = Food()
        self.game_over = False
        
    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))
    
    def draw_score(self):
        score_text = self.font.render(f'Счет: {self.snake.score}', True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))
        
        length_text = self.font.render(f'Длина: {self.snake.grow_to}', True, TEXT_COLOR)
        self.screen.blit(length_text, (10, 40))
    
    def draw_game_over(self):
        game_over_text = self.big_font.render('ИГРА ОКОНЧЕНА!', True, GAME_OVER_COLOR)
        restart_text = self.font.render('Нажмите R для перезапуска', True, TEXT_COLOR)
        quit_text = self.font.render('Нажмите Q для выхода', True, TEXT_COLOR)
        
        self.screen.blit(game_over_text, 
                        (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 
                         WINDOW_HEIGHT // 2 - 60))
        self.screen.blit(restart_text, 
                        (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 
                         WINDOW_HEIGHT // 2))
        self.screen.blit(quit_text, 
                        (WINDOW_WIDTH // 2 - quit_text.get_width() // 2, 
                         WINDOW_HEIGHT // 2 + 40))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if self.game_over:
                    if event.key == K_r:
                        self.restart_game()
                    elif event.key == K_q:
                        pygame.quit()
                        sys.exit()
                else:
                    if event.key == K_UP:
                        self.snake.turn(UP)
                    elif event.key == K_DOWN:
                        self.snake.turn(DOWN)
                    elif event.key == K_LEFT:
                        self.snake.turn(LEFT)
                    elif event.key == K_RIGHT:
                        self.snake.turn(RIGHT)
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
    
    def update(self):
        if not self.game_over:
            # Двигаем змейку
            if not self.snake.move():
                self.game_over = True
                return
            
            # Проверяем, съела ли змейка еду
            if self.snake.get_head_position() == self.food.position:
                self.snake.grow()
                self.food.randomize_position()
                # Убеждаемся, что еда не появляется на змейке
                while self.food.position in self.snake.positions:
                    self.food.randomize_position()
    
    def restart_game(self):
        self.snake.reset()
        self.food.randomize_position()
        self.game_over = False
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            
            # Отрисовка
            self.screen.fill(BACKGROUND_COLOR)
            self.draw_grid()
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            self.draw_score()
            
            if self.game_over:
                self.draw_game_over()
            
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()