import pygame
import sys

# 🔹 Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎮 Pygame Платформер")
clock = pygame.time.Clock()
FPS = 60

# ️ Константы физики
GRAVITY = 0.8
JUMP_FORCE = -15
MOVE_SPEED = 5

# 🎨 Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
BLUE = (100, 149, 237)
GOLD = (255, 215, 0)
DARK_BG = (20, 20, 35)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

    def update(self, platforms):
        # 1. Применяем гравитацию
        self.vel_y += GRAVITY

        # 2. Движение по оси X
        self.rect.x += self.vel_x
        # Разрешение коллизий по X
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel_x > 0:  # Движемся вправо
                    self.rect.right = plat.left
                elif self.vel_x < 0:  # Движемся влево
                    self.rect.left = plat.right

        # 3. Движение по оси Y
        self.rect.y += self.vel_y
        self.on_ground = False
        # Разрешение коллизий по Y
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel_y > 0:  # Падаем вниз
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # Прыгаем вверх и бьёмся головой
                    self.rect.top = plat.bottom
                    self.vel_y = 0

        # Ресет если упал в пропасть
        if self.rect.top > HEIGHT + 100:
            self.respawn()

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_FORCE

    def respawn(self):
        self.rect.topleft = (100, 300)
        self.vel_x = 0
        self.vel_y = 0


# 🗺️ Создание уровня (список прямоугольников-платформ)
platforms = [
    pygame.Rect(0, 550, 800, 50),      # Стартовый пол
    pygame.Rect(300, 450, 200, 20),    # Платформа 1
    pygame.Rect(600, 350, 150, 20),    # Платформа 2
    pygame.Rect(100, 300, 150, 20),    # Платформа 3
    pygame.Rect(400, 200, 200, 20),    # Платформа 4
    pygame.Rect(750, 250, 200, 20),    # Платформа 5
    pygame.Rect(1050, 400, 300, 20),   # Дальняя платформа
    pygame.Rect(1400, 300, 150, 20),   # Высокая платформа
    pygame.Rect(1700, 450, 400, 50),   # Финишная зона
]

#  Цель (золотой флаг)
goal_rect = pygame.Rect(1850, 350, 40, 100)

# 🧍 Игрок
player = Player(100, 400)

# 📷 Камера
camera_x = 0

# 🏁 Состояние игры
running = True
won = False
font = pygame.font.Font(None, 36)

while running:
    # 1️ Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                player.jump()
            if event.key == pygame.K_r and won:
                won = False
                player.respawn()
                camera_x = 0

    # 2️⃣ Управление
    keys = pygame.key.get_pressed()
    player.vel_x = 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.vel_x = -MOVE_SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.vel_x = MOVE_SPEED

    # 3️ Обновление физики
    player.update(platforms)

    # 4️⃣ Проверка победы
    if not won and player.rect.colliderect(goal_rect):
        won = True

    # 5️⃣ Камера (плавное следование за игроком)
    target_cam_x = player.rect.centerx - WIDTH // 2
    camera_x += (target_cam_x - camera_x) * 0.1  # Lerp-сглаживание

    # 6️ Отрисовка
    screen.fill(DARK_BG)

    # Рисуем платформы с учётом смещения камеры
    for plat in platforms:
        draw_rect = plat.copy()
        draw_rect.x -= camera_x
        pygame.draw.rect(screen, GREEN, draw_rect)

    # Рисуем цель
    goal_draw = goal_rect.copy()
    goal_draw.x -= camera_x
    pygame.draw.rect(screen, GOLD, goal_draw)

    # Рисуем игрока
    player_draw = player.rect.copy()
    player_draw.x -= camera_x
    pygame.draw.rect(screen, BLUE, player_draw)

    # Интерфейс
    if won:
        text = font.render("🏆 ПОБЕДА! Нажмите R для рестарта", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    else:
        hint = font.render("Доберитесь до золотого флага 🚩 | Пробел/W/↑ - прыжок", True, WHITE)
        screen.blit(hint, (20, 20))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()