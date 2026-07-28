import pygame
import random
import sys
import os

# --- Инициализация ---
pygame.init()

# --- Настройки экрана ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
YELLOW = (255, 255, 0)

# --- НАСТРОЙКИ СПРАЙТОВ ---
# ВНИМАНИЕ: Имена файлов должны совпадать точь-в-точь (учитывая регистр и .png/.jpg)
SPRITE_DIR = "sprites"  # Имя папки

# Укажите здесь точные имена ваших файлов:
PLAYER_IMG_NAME = "player.png"
ENEMY_IMG_NAME  = "enemy.png"
BULLET_IMG_NAME = "bullet.png"

# Полные пути к файлам
PLAYER_PATH = os.path.join(SPRITE_DIR, PLAYER_IMG_NAME)
ENEMY_PATH  = os.path.join(SPRITE_DIR, ENEMY_IMG_NAME)
BULLET_PATH = os.path.join(SPRITE_DIR, BULLET_IMG_NAME)

def load_image(path, width, height, fallback_color):
    """
    Загружает картинку. Если не получается - рисует цветной квадрат.
    Выводит сообщение в консоль при ошибке.
    """
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (width, height))
            return img
        except pygame.error as e:
            print(f"ОШИБКА загрузки {path}: {e}")
    else:
        print(f"ВНИМАНИЕ: Файл не найден по пути: {path}")
        print("-> Игра использует запасной вариант (цветной квадрат).")
    
    # Если не загрузилось, возвращаем цветной квадрат
    surf = pygame.Surface((width, height))
    surf.fill(fallback_color)
    return surf

# --- Классы ---

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Размер 40x40
        self.image = load_image(PLAYER_PATH, 40, 40, GREEN) 
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed_x = -7
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed_x = 7
        
        self.rect.x += self.speed_x
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0: self.rect.left = 0

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.top)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Размер 5x15
        self.image = load_image(BULLET_PATH, 5, 15, YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_multiplier=1):
        super().__init__()
        size = random.randint(30, 50)
        # Размер меняется случайно
        self.image = load_image(ENEMY_PATH, size, size, RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(2, 5) * speed_multiplier

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.kill()

# --- Звезды на фоне ---
class Star:
    def __init__(self):
        self.x = random.randrange(0, SCREEN_WIDTH)
        self.y = random.randrange(0, SCREEN_HEIGHT)
        self.speed = random.uniform(0.2, 1.0)
        self.size = random.randint(1, 2)
    
    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randrange(0, SCREEN_WIDTH)

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.size)

# --- Интерфейс ---
def draw_text(surf, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# --- Основной цикл ---
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Космический защитник")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    stars = [Star() for _ in range(50)]

    score = 0
    spawn_timer = 0
    spawn_rate = 60
    game_over = False
    difficulty = 1.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_over:
                        b = player.shoot()
                        bullets.add(b)
                        all_sprites.add(b)
                    else:
                        # Рестарт
                        game_over = False
                        score = 0
                        difficulty = 1.0
                        spawn_rate = 60
                        enemies.empty()
                        bullets.empty()
                        all_sprites.empty()
                        all_sprites.add(player)
                        player.rect.centerx = SCREEN_WIDTH // 2
                        player.rect.bottom = SCREEN_HEIGHT - 10

        if not game_over:
            all_sprites.update()
            for star in stars: star.update()

            spawn_timer += 1
            if spawn_timer >= spawn_rate:
                spawn_timer = 0
                enemy = Enemy(speed_multiplier=difficulty)
                enemies.add(enemy)
                all_sprites.add(enemy)
                if spawn_rate > 20: spawn_rate -= 0.5
                difficulty += 0.01

            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            score += len(hits) * 10

            if pygame.sprite.spritecollideany(player, enemies):
                game_over = True

        # Отрисовка
        screen.fill(BLACK)
        for star in stars: star.draw(screen)
        all_sprites.draw(screen)
        draw_text(screen, f"Счет: {score}", 30, SCREEN_WIDTH / 2, 10)

        if game_over:
            draw_text(screen, "ИГРА ОКОНЧЕНА", 60, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20, RED)
            draw_text(screen, "ПРОБЕЛ - рестарт", 30, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40, WHITE)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()