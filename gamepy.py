import pygame
import sys
import random
import json
import os
from enum import Enum

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Константы экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (0, 255, 0)
BLUE = (50, 100, 255)
YELLOW = (255, 255, 0)
PURPLE = (150, 50, 200)
ORANGE = (255, 165, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
LIGHT_BLUE = (100, 150, 255)

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Collection - Змейка, Пинг-понг, Арканоид")
clock = pygame.time.Clock()

# Шрифты
font_small = pygame.font.Font(None, 36)
font_medium = pygame.font.Font(None, 48)
font_big = pygame.font.Font(None, 72)
font_title = pygame.font.Font(None, 96)

# Файл для сохранения рекордов
RECORDS_FILE = "game_records.json"

def load_records():
    """Загрузка рекордов из файла"""
    if os.path.exists(RECORDS_FILE):
        try:
            with open(RECORDS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {"snake": {level: 0 for level in range(1, 11)}, "pong": 0, "arkanoid": 0}

def save_records(records):
    """Сохранение рекордов в файл"""
    try:
        with open(RECORDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    except:
        pass

class Button:
    """Класс кнопки меню"""
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
    
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10)
        
        text_surface = font_medium.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False

class SnakeGame:
    """Игра Змейка с 10 уровнями сложности"""
    
    # Уровни сложности: (название, скорость падения (мс на кадр))
    LEVELS = {
        1: ("Нуб", 180),
        2: ("Легкий", 150),
        3: ("Средний", 130),
        4: ("Продвинутый", 110),
        5: ("Сложный", 95),
        6: ("Эксперт", 80),
        7: ("Мастер", 70),
        8: ("Грандмастер", 60),
        9: ("Легенда", 50),
        10: ("Бог", 40)
    }
    
    def __init__(self, level=1):
        self.cell_size = 20
        self.grid_width = SCREEN_WIDTH // self.cell_size
        self.grid_height = SCREEN_HEIGHT // self.cell_size
        self.level = level
        self.level_name, self.speed_ms = self.LEVELS[level]
        self.reset_game()
    
    def reset_game(self):
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.game_over = False
        self.last_move_time = pygame.time.get_ticks()
        self.generate_food()
    
    def generate_food(self):
        while True:
            food_pos = (random.randint(0, self.grid_width - 1),
                       random.randint(0, self.grid_height - 1))
            if food_pos not in self.snake:
                self.food = food_pos
                break
    
    def update(self):
        if self.game_over:
            return
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.speed_ms:
            self.last_move_time = current_time
            self.move_snake()
    
    def move_snake(self):
        self.direction = self.next_direction
        
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Проверка столкновения со стенами
        if (new_head[0] < 0 or new_head[0] >= self.grid_width or
            new_head[1] < 0 or new_head[1] >= self.grid_height):
            self.game_over = True
            return
        
        # Проверка столкновения с собой
        if new_head in self.snake:
            self.game_over = True
            return
        
        self.snake.insert(0, new_head)
        
        if new_head == self.food:
            self.score += 1
            self.generate_food()
        else:
            self.snake.pop()
    
    def change_direction(self, new_dir):
        opposites = {(1, 0): (-1, 0), (-1, 0): (1, 0),
                    (0, 1): (0, -1), (0, -1): (0, 1)}
        if new_dir != opposites.get(self.direction, new_dir):
            self.next_direction = new_dir
    
    def draw(self, surface):
        surface.fill(BLACK)
        
        # Рисуем змейку
        for i, segment in enumerate(self.snake):
            color = GREEN if i == 0 else LIGHT_BLUE
            rect = pygame.Rect(segment[0] * self.cell_size,
                              segment[1] * self.cell_size,
                              self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, WHITE, rect, 1)
        
        # Рисуем еду
        food_rect = pygame.Rect(self.food[0] * self.cell_size,
                               self.food[1] * self.cell_size,
                               self.cell_size - 1, self.cell_size - 1)
        pygame.draw.rect(surface, RED, food_rect)
        
        # Счёт
        score_text = font_small.render(f"Счёт: {self.score}", True, WHITE)
        surface.blit(score_text, (10, 10))
        
        # Уровень сложности
        level_text = font_small.render(f"Уровень: {self.level_name} ({self.level})", True, YELLOW)
        surface.blit(level_text, (SCREEN_WIDTH - 250, 10))
        
        # Скорость (кадров в секунду ≈ 1000/скорость)
        speed_display = int(1000 / self.speed_ms)
        speed_text = font_small.render(f"Скорость: {speed_display} кадров/сек", True, GRAY)
        surface.blit(speed_text, (SCREEN_WIDTH - 250, 40))
        
        if self.game_over:
            game_over_text = font_medium.render("ИГРА ОКОНЧЕНА", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            surface.blit(game_over_text, text_rect)
            
            restart_text = font_small.render("Нажмите ПРОБЕЛ для новой игры или ESC для выхода", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            surface.blit(restart_text, restart_rect)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.change_direction((0, -1))
            elif event.key == pygame.K_DOWN:
                self.change_direction((0, 1))
            elif event.key == pygame.K_LEFT:
                self.change_direction((-1, 0))
            elif event.key == pygame.K_RIGHT:
                self.change_direction((1, 0))
            elif event.key == pygame.K_SPACE and self.game_over:
                self.reset_game()
            elif event.key == pygame.K_ESCAPE:
                return "exit"
        return None

class PongGame:
    """Игра Пинг-понг (2 игрока или против бота)"""
    def __init__(self, vs_bot=True):
        self.paddle_width = 15
        self.paddle_height = 100
        self.ball_size = 15
        self.reset_game(vs_bot)
    
    def reset_game(self, vs_bot=None):
        if vs_bot is not None:
            self.vs_bot = vs_bot
        
        self.left_paddle = pygame.Rect(30, SCREEN_HEIGHT // 2 - self.paddle_height // 2,
                                       self.paddle_width, self.paddle_height)
        self.right_paddle = pygame.Rect(SCREEN_WIDTH - 30 - self.paddle_width,
                                        SCREEN_HEIGHT // 2 - self.paddle_height // 2,
                                        self.paddle_width, self.paddle_height)
        
        self.ball = pygame.Rect(SCREEN_WIDTH // 2 - self.ball_size // 2,
                                SCREEN_HEIGHT // 2 - self.ball_size // 2,
                                self.ball_size, self.ball_size)
        
        self.ball_speed_x = 5 * random.choice([-1, 1])
        self.ball_speed_y = 5 * random.choice([-1, 1])
        self.score_left = 0
        self.score_right = 0
        self.game_over = False
        self.winner = None
    
    def update(self):
        if self.game_over:
            return
        
        # Движение мяча
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y
        
        # Отскок от верха и низа
        if self.ball.top <= 0 or self.ball.bottom >= SCREEN_HEIGHT:
            self.ball_speed_y *= -1
        
        # Отскок от левой ракетки
        if self.ball.colliderect(self.left_paddle):
            self.ball_speed_x = abs(self.ball_speed_x)
            hit_pos = (self.ball.centery - self.left_paddle.centery) / (self.paddle_height / 2)
            self.ball_speed_y = 5 * hit_pos
            self.ball_speed_x += 0.5
        
        # Отскок от правой ракетки
        if self.ball.colliderect(self.right_paddle):
            self.ball_speed_x = -abs(self.ball_speed_x)
            hit_pos = (self.ball.centery - self.right_paddle.centery) / (self.paddle_height / 2)
            self.ball_speed_y = 5 * hit_pos
            self.ball_speed_x -= 0.5
        
        # Голы
        if self.ball.left <= 0:
            self.score_right += 1
            self.reset_ball()
        elif self.ball.right >= SCREEN_WIDTH:
            self.score_left += 1
            self.reset_ball()
        
        # Проверка победы (до 7 очков)
        if self.score_left >= 7:
            self.game_over = True
            self.winner = "left"
        elif self.score_right >= 7:
            self.game_over = True
            self.winner = "right"
        
        self.move_paddles()
    
    def reset_ball(self):
        self.ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.ball_speed_x = 5 * random.choice([-1, 1])
        self.ball_speed_y = 5 * random.choice([-1, 1])
        pygame.time.wait(500)
    
    def move_paddles(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w] and self.left_paddle.top > 0:
            self.left_paddle.y -= 7
        if keys[pygame.K_s] and self.left_paddle.bottom < SCREEN_HEIGHT:
            self.left_paddle.y += 7
        
        if self.vs_bot:
            if self.right_paddle.centery < self.ball.centery - 20:
                self.right_paddle.y += 5
            elif self.right_paddle.centery > self.ball.centery + 20:
                self.right_paddle.y -= 5
            if self.right_paddle.top < 0:
                self.right_paddle.top = 0
            if self.right_paddle.bottom > SCREEN_HEIGHT:
                self.right_paddle.bottom = SCREEN_HEIGHT
        else:
            if keys[pygame.K_UP] and self.right_paddle.top > 0:
                self.right_paddle.y -= 7
            if keys[pygame.K_DOWN] and self.right_paddle.bottom < SCREEN_HEIGHT:
                self.right_paddle.y += 7
    
    def draw(self, surface):
        surface.fill(BLACK)
        
        for y in range(0, SCREEN_HEIGHT, 30):
            pygame.draw.rect(surface, WHITE, (SCREEN_WIDTH // 2 - 5, y, 10, 15))
        
        pygame.draw.rect(surface, BLUE, self.left_paddle)
        pygame.draw.rect(surface, RED, self.right_paddle)
        pygame.draw.ellipse(surface, WHITE, self.ball)
        
        score_text = font_big.render(f"{self.score_left}   {self.score_right}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        surface.blit(score_text, score_rect)
        
        mode_text = font_small.render("Против бота" if self.vs_bot else "2 игрока", True, GRAY)
        surface.blit(mode_text, (SCREEN_WIDTH - 150, 10))
        
        if self.game_over:
            winner_text = "Левый игрок победил!" if self.winner == "left" else "Правый игрок победил!"
            game_over_text = font_medium.render(winner_text, True, YELLOW)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            surface.blit(game_over_text, text_rect)
            
            restart_text = font_small.render("Нажмите ПРОБЕЛ для новой игры или ESC для выхода", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            surface.blit(restart_text, restart_rect)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.game_over:
                self.reset_game()
                return "restart"
            elif event.key == pygame.K_ESCAPE:
                return "exit"
        return None

class ArkanoidGame:
    """Игра Арканоид"""
    def __init__(self):
        self.paddle_width = 120
        self.paddle_height = 15
        self.ball_size = 12
        self.brick_width = 70
        self.brick_height = 25
        self.reset_game()
    
    def reset_game(self):
        self.paddle = pygame.Rect(SCREEN_WIDTH // 2 - self.paddle_width // 2,
                                  SCREEN_HEIGHT - 50,
                                  self.paddle_width, self.paddle_height)
        
        self.ball = pygame.Rect(SCREEN_WIDTH // 2 - self.ball_size // 2,
                                SCREEN_HEIGHT - 80,
                                self.ball_size, self.ball_size)
        
        self.ball_speed_x = 4 * random.choice([-1, 1])
        self.ball_speed_y = -4
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.winner = False
        self.create_bricks()
    
    def create_bricks(self):
        self.bricks = []
        offset_x = (SCREEN_WIDTH - (self.brick_width + 5) * 10) // 2
        for row in range(5):
            for col in range(10):
                brick = pygame.Rect(offset_x + col * (self.brick_width + 5),
                                   50 + row * (self.brick_height + 5),
                                   self.brick_width, self.brick_height)
                self.bricks.append(brick)
    
    def update(self):
        if self.game_over:
            return
        
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y
        
        if self.ball.left <= 0 or self.ball.right >= SCREEN_WIDTH:
            self.ball_speed_x *= -1
        if self.ball.top <= 0:
            self.ball_speed_y *= -1
        
        if self.ball.colliderect(self.paddle):
            self.ball_speed_y = -abs(self.ball_speed_y)
            hit_pos = (self.ball.centerx - self.paddle.centerx) / (self.paddle_width / 2)
            self.ball_speed_x = 4 * hit_pos
        
        for brick in self.bricks[:]:
            if self.ball.colliderect(brick):
                self.bricks.remove(brick)
                self.ball_speed_y *= -1
                self.score += 10
        
        if self.ball.top >= SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
                self.winner = False
            else:
                self.reset_ball()
        
        if len(self.bricks) == 0:
            self.game_over = True
            self.winner = True
    
    def reset_ball(self):
        self.ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
        self.ball_speed_x = 4 * random.choice([-1, 1])
        self.ball_speed_y = -4
        pygame.time.wait(500)
    
    def draw(self, surface):
        surface.fill(BLACK)
        
        pygame.draw.rect(surface, BLUE, self.paddle)
        pygame.draw.ellipse(surface, WHITE, self.ball)
        
        for brick in self.bricks:
            color = [RED, ORANGE, YELLOW, GREEN, BLUE][brick.y // 30 % 5]
            pygame.draw.rect(surface, color, brick)
            pygame.draw.rect(surface, WHITE, brick, 2)
        
        score_text = font_small.render(f"Счёт: {self.score}", True, WHITE)
        surface.blit(score_text, (10, 10))
        
        lives_text = font_small.render(f"Жизни: {self.lives}", True, RED)
        surface.blit(lives_text, (SCREEN_WIDTH - 120, 10))
        
        if self.game_over:
            if self.winner:
                result_text = font_medium.render("ПОБЕДА!", True, GREEN)
            else:
                result_text = font_medium.render("ИГРА ОКОНЧЕНА", True, RED)
            text_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            surface.blit(result_text, text_rect)
            
            restart_text = font_small.render("Нажмите ПРОБЕЛ для новой игры или ESC для выхода", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            surface.blit(restart_text, restart_rect)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.game_over:
                self.reset_game()
                return "restart"
            elif event.key == pygame.K_ESCAPE:
                return "exit"
        return None
    
    def move_paddle(self, x):
        self.paddle.x += x
        if self.paddle.left < 0:
            self.paddle.left = 0
        if self.paddle.right > SCREEN_WIDTH:
            self.paddle.right = SCREEN_WIDTH

class GameMenu:
    """Главное меню игры"""
    def __init__(self):
        self.records = load_records()
        self.running = True
        self.current_game = None
        self.buttons = []
        self.create_buttons()
    
    def create_buttons(self):
        button_width = 250
        button_height = 60
        start_y = 200
        spacing = 80
        
        self.buttons = [
            Button(SCREEN_WIDTH // 2 - button_width // 2, start_y, 
                   button_width, button_height, "🐍 Змейка", GREEN, LIGHT_BLUE),
            Button(SCREEN_WIDTH // 2 - button_width // 2, start_y + spacing,
                   button_width, button_height, "🏓 Пинг-понг", BLUE, LIGHT_BLUE),
            Button(SCREEN_WIDTH // 2 - button_width // 2, start_y + spacing * 2,
                   button_width, button_height, "🧱 Арканоид", PURPLE, LIGHT_BLUE),
            Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 80,
                   200, 50, "Выход", RED, ORANGE)
        ]
    
    def draw(self):
        screen.fill(BLACK)
        
        title_text = font_title.render("GAME COLLECTION", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)
        
        # Отображаем лучшие рекорды по уровням для змейки
        best_snake = max(self.records["snake"].values())
        records_text = font_small.render(f"Рекорды: Змейка (лучший): {best_snake}  |  "
                                         f"Пинг-понг: {self.records['pong']}  |  "
                                         f"Арканоид: {self.records['arkanoid']}", True, GRAY)
        records_rect = records_text.get_rect(center=(SCREEN_WIDTH // 2, 160))
        screen.blit(records_text, records_rect)
        
        for button in self.buttons:
            button.draw(screen)
    
    def run_snake_level_selection(self):
        """Выбор уровня сложности для змейки"""
        level_buttons = []
        for level in range(1, 11):
            name, _ = SnakeGame.LEVELS[level]
            btn = Button(SCREEN_WIDTH // 2 - 150, 150 + (level-1) * 45, 300, 40,
                        f"{level}. {name}", DARK_GRAY, LIGHT_BLUE)
            level_buttons.append((level, btn))
        
        back_btn = Button(SCREEN_WIDTH // 2 - 100, 600, 200, 50, "Назад", RED, ORANGE)
        
        selecting = True
        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                for level, btn in level_buttons:
                    if btn.handle_event(event):
                        return level
                if back_btn.handle_event(event):
                    return None
            
            screen.fill(BLACK)
            title_text = font_medium.render("Выберите уровень сложности", True, YELLOW)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
            screen.blit(title_text, title_rect)
            
            description_text = font_small.render("Чем выше уровень, тем быстрее змейка", True, GRAY)
            desc_rect = description_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
            screen.blit(description_text, desc_rect)
            
            for _, btn in level_buttons:
                btn.draw(screen)
            back_btn.draw(screen)
            
            pygame.display.flip()
            clock.tick(FPS)
    
    def run_pong_mode_selection(self):
        """Выбор режима для пинг-понга"""
        vs_bot_btn = Button(SCREEN_WIDTH // 2 - 150, 250, 300, 60,
                           "Против бота", BLUE, LIGHT_BLUE)
        vs_friend_btn = Button(SCREEN_WIDTH // 2 - 150, 350, 300, 60,
                              "2 игрока", GREEN, LIGHT_BLUE)
        back_btn = Button(SCREEN_WIDTH // 2 - 100, 450, 200, 50,
                         "Назад", RED, ORANGE)
        
        selecting = True
        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if vs_bot_btn.handle_event(event):
                    return True
                if vs_friend_btn.handle_event(event):
                    return False
                if back_btn.handle_event(event):
                    return None
            
            screen.fill(BLACK)
            title_text = font_medium.render("Выберите режим игры", True, YELLOW)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            screen.blit(title_text, title_rect)
            
            vs_bot_btn.draw(screen)
            vs_friend_btn.draw(screen)
            back_btn.draw(screen)
            
            pygame.display.flip()
            clock.tick(FPS)
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                for i, button in enumerate(self.buttons):
                    if button.handle_event(event):
                        if i == 0:  # Змейка
                            level = self.run_snake_level_selection()
                            if level is not None:
                                self.current_game = "snake"
                                game = SnakeGame(level=level)
                                self.run_game(game, "snake", level)
                        elif i == 1:  # Пинг-понг
                            mode = self.run_pong_mode_selection()
                            if mode is not None:
                                self.current_game = "pong"
                                game = PongGame(vs_bot=mode)
                                self.run_game(game, "pong")
                        elif i == 2:  # Арканоид
                            self.current_game = "arkanoid"
                            game = ArkanoidGame()
                            self.run_game(game, "arkanoid")
                        elif i == 3:  # Выход
                            self.running = False
            
            self.draw()
            pygame.display.flip()
            clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def run_game(self, game, game_type, level=None):
        """Запуск выбранной игры"""
        running = True
        while running:
            if game_type == "arkanoid":
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    game.move_paddle(-8)
                if keys[pygame.K_RIGHT]:
                    game.move_paddle(8)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                result = game.handle_event(event)
                if result == "exit":
                    running = False
                elif result == "restart":
                    self.update_record(game, game_type, level)
            
            if game_type == "arkanoid":
                game.update()
            elif game_type == "snake":
                game.update()
            elif game_type == "pong":
                game.update()
            
            game.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
        
        self.update_record(game, game_type, level)
    
    def update_record(self, game, game_type, level=None):
        """Обновление рекорда"""
        if game_type == "snake" and level is not None:
            if game.score > self.records["snake"].get(level, 0):
                self.records["snake"][level] = game.score
                save_records(self.records)
        elif game_type == "pong" and max(game.score_left, game.score_right) > self.records["pong"]:
            self.records["pong"] = max(game.score_left, game.score_right)
            save_records(self.records)
        elif game_type == "arkanoid" and game.score > self.records["arkanoid"]:
            self.records["arkanoid"] = game.score
            save_records(self.records)

if __name__ == "__main__":
    menu = GameMenu()
    menu.run()