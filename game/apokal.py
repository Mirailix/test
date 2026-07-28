import pygame
import random
import sys
import time

# -------------------- CONFIG --------------------
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 60

# Grid settings
GRID_ROWS = 15
GRID_COLS = 20
CELL_SIZE = 32

# Colors (R,G,B)
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
RED     = (200, 0, 0)
GREEN   = (0, 200, 0)
BLUE    = (0, 0, 200)
GRAY    = (100, 100, 100)
ORANGE  = (255, 165, 0)

# -------------------- HELPERS --------------------
def clamp(val, min_val, max_val):
    return max(min_val, min(val, max_val))

# -------------------- GAME OBJECTS --------------------
class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE - 4, CELL_SIZE - 4))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = start_pos
        self.speed = 4

    def update(self, walls):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed

        # Horizontal movement
        self.rect.x += dx
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.x -= dx

        # Vertical movement
        self.rect.y += dy
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.y -= dy

class Zombie(pygame.sprite.Sprite):
    def __init__(self, start_pos, target):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE - 6, CELL_SIZE - 6))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.speed = 1.5
        self.target = target  # reference to Player

    def update(self, walls):
        # Simple steering: move horizontally then vertically
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        dist = (dx**2 + dy**2)**0.5
        if dist == 0:
            return
        dx, dy = dx / dist, dy / dist  # normalize

        # Try horizontal first
        self.rect.x += dx * self.speed
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.x -= dx * self.speed

        # Then vertical
        self.rect.y += dy * self.speed
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.y -= dy * self.speed



class Wall(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

class Exit(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

# -------------------- GAME SETUP --------------------
def create_grid():
    """Return a list of wall positions."""
    walls = []
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            # Border walls
            if r == 0 or r == GRID_ROWS - 1 or c == 0 or c == GRID_COLS - 1:
                walls.append((c * CELL_SIZE, r * CELL_SIZE))
            # Random internal walls (~20%)
            elif random.random() < 0.2:
                walls.append((c * CELL_SIZE, r * CELL_SIZE))
    return walls

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Zombie Escape – Post‑Apocalypse")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    # --- Create sprite groups ---
    walls_sprites = pygame.sprite.Group()
    zombies_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    # --- Place walls ---
    wall_positions = create_grid()
    for pos in wall_positions:
        w = Wall(pos)
        walls_sprites.add(w)
        all_sprites.add(w)

    # --- Place exit (bottom‑right corner) ---
    exit_pos = (GRID_COLS - 2) * CELL_SIZE, (GRID_ROWS - 2) * CELL_SIZE
    exit_door = Exit(exit_pos)
    all_sprites.add(exit_door)

    # --- Create player (top‑left corner) ---
    player_start = CELL_SIZE, CELL_SIZE
    player = Player(player_start)
    all_sprites.add(player)

    # --- Spawn zombies (5 at random free spots) ---
    def random_free_cell():
        while True:
            r = random.randint(1, GRID_ROWS - 2)
            c = random.randint(1, GRID_COLS - 2)
            pos = (c * CELL_SIZE, r * CELL_SIZE)
            # Avoid walls, exit, or player
            if pos != player_start and pos != exit_pos and pos not in wall_positions:
                return pos

    for _ in range(5):
        z_pos = random_free_cell()
        z = Zombie(z_pos, player)
        zombies_sprites.add(z)
        all_sprites.add(z)

    # --- Game state ---
    start_time = time.time()
    running = True
    game_over = False
    win = False

    # -------------------- MAIN LOOP --------------------
    while running:
        dt = clock.tick(FPS) / 1000.0  # seconds per frame

        # ----- Event Handling -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        if not game_over and not win:
            # ----- Update Sprites -----
            player.update(walls_sprites)
            zombies_sprites.update(walls_sprites)

            # ----- Collision Checks -----
            if pygame.sprite.spritecollideany(player, zombies_sprites):
                game_over = True
            if pygame.sprite.collide_rect(player, exit_door):
                win = True

        # ----- Rendering -----
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # HUD
        elapsed = int(time.time() - start_time)
        hud_text = f"Time: {elapsed}s  Zombies: {len(zombies_sprites)}  FPS: {clock.get_fps():.1f}"
        hud_surface = font.render(hud_text, True, ORANGE)
        screen.blit(hud_surface, (10, 10))

        if game_over:
            msg = font.render("GAME OVER! Press ESC to quit.", True, RED)
            screen.blit(msg, (WINDOW_WIDTH // 2 - msg.get_width() // 2,
                              WINDOW_HEIGHT // 2 - msg.get_height() // 2))
        if win:
            msg = font.render("YOU ESCAPED! Congratulations!", True, GREEN)
            screen.blit(msg, (WINDOW_WIDTH // 2 - msg.get_width() // 2,
                              WINDOW_HEIGHT // 2 - msg.get_height() // 2))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# -------------------- ENTRY POINT --------------------
if __name__ == "__main__":
    main()