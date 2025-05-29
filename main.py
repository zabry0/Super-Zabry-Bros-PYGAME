import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Zabry Bros - Více levelů")

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)

def load_image(path, scale=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        if scale:
            img = pygame.transform.scale(img, scale)
        return img
    except pygame.error:
        print(f"Chyba: obrázek {path} nenalezen.")
        return None

background = load_image("background.png", (WIDTH, HEIGHT))
player_img = load_image("player.png", (64, 64))
enemy_img = load_image("enemy.png", (64, 64))
platform_img = load_image("platform.png", (128, 32))

class Player:
    def __init__(self):
        self.image = player_img
        self.rect = self.image.get_rect() if self.image else pygame.Rect(50, HEIGHT - 150, 64, 64)
        self.rect.topleft = (50, HEIGHT - 150)
        self.vel_y = 0
        self.speed = 5
        self.jumping = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        if not self.jumping and keys[pygame.K_SPACE]:
            self.vel_y = -15
            self.jumping = True

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        self.rect.y += self.vel_y

        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y >= 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.jumping = False

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, (0, 255, 0), self.rect)

class Platform:
    def __init__(self, x, y):
        self.image = platform_img
        self.rect = self.image.get_rect() if self.image else pygame.Rect(x, y, 128, 32)
        self.rect.topleft = (x, y)

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, (100, 100, 100), self.rect)

class Enemy:
    def __init__(self, x, y, path_length=150):
        self.image = enemy_img
        self.rect = self.image.get_rect() if self.image else pygame.Rect(x, y, 64, 64)
        self.rect.topleft = (x, y)
        self.path_length = path_length
        self.start_x = x
        self.speed = 3
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if abs(self.rect.x - self.start_x) > self.path_length:
            self.direction *= -1

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, (255, 0, 0), self.rect)

levels = [
    {
        "platforms": [
            (0, HEIGHT - 40),
            (200, HEIGHT - 150),
            (400, HEIGHT - 300),
            (600, HEIGHT - 220),
            (350, HEIGHT - 100)
        ],
        "enemies": [
            (220, HEIGHT - 190),
            (420, HEIGHT - 340)
        ]
    },
    {
        "platforms": [
            (0, HEIGHT - 40),
            (150, HEIGHT - 200),
            (350, HEIGHT - 250),
            (550, HEIGHT - 320),
            (700, HEIGHT - 150),
            (400, HEIGHT - 100)
        ],
        "enemies": [
            (160, HEIGHT - 240),
            (560, HEIGHT - 360),
            (720, HEIGHT - 190)
        ]
    },
    {
        "platforms": [
            (0, HEIGHT - 40),
            (250, HEIGHT - 180),
            (500, HEIGHT - 280),
            (750, HEIGHT - 220),
            (600, HEIGHT - 120),
            (350, HEIGHT - 90)
        ],
        "enemies": [
            (260, HEIGHT - 220),
            (510, HEIGHT - 320),
            (760, HEIGHT - 260),
            (610, HEIGHT - 160)
        ]
    }
]

def load_level(level_data):
    platforms = [Platform(x, y) for x, y in level_data["platforms"]]
    enemies = [Enemy(x, y) for x, y in level_data["enemies"]]
    return platforms, enemies

def main():
    player = Player()
    current_level = 0
    platforms, enemies = load_level(levels[current_level])
    font = pygame.font.SysFont("Consolas", 36)

    game_over = False
    victory = False

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over and not victory:
            player.update(platforms)
            for enemy in enemies:
                enemy.update()

            # Kontrola kolize s nepřáteli
            for enemy in enemies:
                if player.rect.colliderect(enemy.rect):
                    game_over = True

            # Přechod do dalšího levelu
            if player.rect.right >= WIDTH - 10:
                current_level += 1
                if current_level >= len(levels):
                    victory = True
                else:
                    platforms, enemies = load_level(levels[current_level])
                    player.rect.topleft = (50, HEIGHT - 150)

            # Kontrola pádu do voidu - restart levelu
            if player.rect.top > HEIGHT:
                platforms, enemies = load_level(levels[current_level])
                player.rect.topleft = (50, HEIGHT - 150)

        keys = pygame.key.get_pressed()
        if game_over or victory:
            if keys[pygame.K_r]:
                current_level = 0
                platforms, enemies = load_level(levels[current_level])
                player.rect.topleft = (50, HEIGHT - 150)
                game_over = False
                victory = False

        # Vykreslení
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((30, 30, 50))

        for platform in platforms:
            platform.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)

        player.draw(screen)

        if game_over:
            text = font.render("GAME OVER - Stiskni R pro restart", True, (255, 50, 50))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))

        if victory:
            text = font.render("VYHRÁL JSI! Stiskni R pro restart", True, (50, 255, 50))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))

        pygame.display.flip()

if __name__ == "__main__":
    main()
