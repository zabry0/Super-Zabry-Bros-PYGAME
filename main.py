import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Zabry Bros - 7 úrovní")

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

background1 = load_image("background.png", (WIDTH, HEIGHT))
background2 = load_image("background2.png", (WIDTH, HEIGHT))
background3 = load_image("background3.png", (WIDTH, HEIGHT))
player_img = load_image("player.png", (64, 64))
enemy_img = load_image("enemy.png", (64, 64))
platform_img = load_image("platform.png", (128, 32))

def draw_text_with_bg(surface, text, font, color, y):
    rendered = font.render(text, True, color)
    bg_rect = rendered.get_rect(center=(WIDTH//2, y + rendered.get_height()//2))
    s = pygame.Surface((bg_rect.width + 20, bg_rect.height + 10), pygame.SRCALPHA)
    s.fill((0, 0, 0, 150))  # černé poloprůhledné pozadí
    surface.blit(s, (bg_rect.left - 10, bg_rect.top - 5))
    surface.blit(rendered, (bg_rect.left, bg_rect.top))

def draw_lives(surface, lives):
    heart = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.polygon(heart, (255, 0, 0), [(10,0),(20,7),(15,20),(10,15),(5,20),(0,7)])
    for i in range(lives):
        surface.blit(heart, (10 + i*30, 10))

class Player:
    def __init__(self):
        self.image = player_img
        self.rect = self.image.get_rect() if self.image else pygame.Rect(50, HEIGHT - 150, 64, 64)
        self.rect.topleft = (50, HEIGHT - 150)
        self.vel_y = 0
        self.speed = 5
        self.jumping = False
        self.lives = 3

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        if not self.jumping and keys[pygame.K_w]:
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

# Celkem 7 levelů, poslední dva jsou těžké s background3.png
levels = [
    # Level 1 - background1
    {
        "background": background1,
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
    # Level 2 - background1
    {
        "background": background1,
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
    # Level 3 - background1
    {
        "background": background1,
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
    },
    # Level 4 - background2
    {
        "background": background2,
        "platforms": [
            (0, HEIGHT - 40),
            (100, HEIGHT - 200),
            (300, HEIGHT - 240),
            (550, HEIGHT - 300),
            (700, HEIGHT - 160),
            (400, HEIGHT - 120)
        ],
        "enemies": [
            (110, HEIGHT - 240),
            (310, HEIGHT - 280),
            (560, HEIGHT - 340),
            (710, HEIGHT - 200)
        ]
    },
    # Level 5 - background2
    {
        "background": background2,
        "platforms": [
            (0, HEIGHT - 40),
            (200, HEIGHT - 210),
            (450, HEIGHT - 260),
            (700, HEIGHT - 310),
            (600, HEIGHT - 130),
            (350, HEIGHT - 100)
        ],
        "enemies": [
            (210, HEIGHT - 250),
            (460, HEIGHT - 300),
            (710, HEIGHT - 350),
            (610, HEIGHT - 170)
        ]
    },
    # Level 6 - HARD - background3
    {
        "background": background3,
        "platforms": [
            (0, HEIGHT - 40),
            (250, HEIGHT - 220),
            (500, HEIGHT - 280),
            (650, HEIGHT - 320),
            (750, HEIGHT - 150),
            (400, HEIGHT - 110)
        ],
        "enemies": [
            (260, HEIGHT - 260),
            (510, HEIGHT - 320),
            (660, HEIGHT - 360),
            (760, HEIGHT - 190)
        ]
    },
    # Level 7 - HARD - background3
    {
        "background": background3,
        "platforms": [
            (0, HEIGHT - 40),
            (150, HEIGHT - 230),
            (350, HEIGHT - 280),
            (550, HEIGHT - 320),
            (700, HEIGHT - 180),
            (400, HEIGHT - 140)
        ],
        "enemies": [
            (160, HEIGHT - 270),
            (360, HEIGHT - 320),
            (560, HEIGHT - 360),
            (710, HEIGHT - 220)
        ]
    }
]

def load_level(level_data):
    platforms = [Platform(x, y) for x, y in level_data["platforms"]]
    enemies = [Enemy(x, y) for x, y in level_data["enemies"]]
    background = level_data.get("background", None)
    return platforms, enemies, background

def draw_text_center(surface, text, font, color, y):
    rendered = font.render(text, True, color)
    surface.blit(rendered, (WIDTH//2 - rendered.get_width()//2, y))

def main():
    player = Player()
    current_level = 0
    platforms, enemies, current_background = load_level(levels[current_level])
    font = pygame.font.SysFont("Consolas", 36)
    small_font = pygame.font.SysFont("Consolas", 24)

    game_over = False
    victory = False
    paused = False
    screen_state = "intro"
    show_hard_message = False
    hard_message_timer = 0
    HARD_MESSAGE_DURATION = 180  # frames (~3 seconds)

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and screen_state == "game" and not game_over and not victory:
                    paused = not paused

                if screen_state == "intro" and event.key == pygame.K_RETURN:
                    screen_state = "menu"

                elif screen_state == "menu" and event.key == pygame.K_RETURN:
                    screen_state = "game"

                elif (game_over or victory) and event.key == pygame.K_r:
                    current_level = 0
                    platforms, enemies, current_background = load_level(levels[current_level])
                    player.rect.topleft = (50, HEIGHT - 150)
                    player.lives = 3
                    game_over = False
                    victory = False
                    paused = False
                    screen_state = "game"
                    show_hard_message = False
                    hard_message_timer = 0

        if screen_state == "intro":
            screen.fill((0, 0, 50))
            draw_text_center(screen, "NÁVOD NA OVLÁDÁNÍ", font, WHITE, HEIGHT // 5)
            draw_text_center(screen, "A - pohyb doleva", small_font, WHITE, HEIGHT // 5 + 60)
            draw_text_center(screen, "D - pohyb doprava", small_font, WHITE, HEIGHT // 5 + 100)
            draw_text_center(screen, "W - skok", small_font, WHITE, HEIGHT // 5 + 140)
            draw_text_center(screen, "P - pauza", small_font, WHITE, HEIGHT // 5 + 180)
            draw_text_center(screen, "ENTER - pokračovat", small_font, WHITE, HEIGHT // 5 + 260)
            pygame.display.flip()
            continue

        if screen_state == "menu":
            screen.fill((0, 0, 100))
            draw_text_center(screen, "SUPER ZABRY BROS", font, WHITE, HEIGHT // 3)
            draw_text_center(screen, "Stiskni ENTER pro start", small_font, WHITE, HEIGHT // 2)
            pygame.display.flip()
            continue

        if screen_state == "game":
            if not game_over and not victory and not paused:
                player.update(platforms)
                for enemy in enemies:
                    enemy.update()

                for enemy in enemies:
                    if player.rect.colliderect(enemy.rect):
                        player.lives -= 1
                        if player.lives <= 0:
                            game_over = True
                        else:
                            player.rect.topleft = (50, HEIGHT - 150)

                if player.rect.right >= WIDTH - 10:
                    current_level += 1
                    if current_level >= len(levels):
                        victory = True
                    else:
                        platforms, enemies, current_background = load_level(levels[current_level])
                        player.rect.topleft = (50, HEIGHT - 150)
                        # Po dosažení levelu 6 a 7 zobraz zprávu HARD
                        if current_level == 5 or current_level == 6:
                            show_hard_message = True
                            hard_message_timer = HARD_MESSAGE_DURATION

                if player.rect.top > HEIGHT:
                    player.lives -= 3
                    if player.lives <= 0:
                        game_over = True
                    else:
                        platforms, enemies, current_background = load_level(levels[current_level])
                        player.rect.topleft = (50, HEIGHT - 150)

            if current_background:
                screen.blit(current_background, (0, 0))
            else:
                screen.fill((30, 30, 50))

            for platform in platforms:
                platform.draw(screen)

            for enemy in enemies:
                enemy.draw(screen)

            player.draw(screen)

            draw_lives(screen, player.lives)

            if paused:
                draw_text_with_bg(screen, "PAUZA - Stiskni P pro pokračování", font, (255, 255, 0), HEIGHT // 2)

            if game_over:
                draw_text_with_bg(screen, "GAME OVER - Stiskni R pro restart", font, (255, 50, 50), HEIGHT // 2 - 50)

            if victory:
                draw_text_with_bg(screen, "VYHRÁL JSI! Stiskni R pro restart", font, (50, 255, 50), HEIGHT // 2 - 50)

            if show_hard_message:
                draw_text_with_bg(screen, "HARD ÚROVEŇ!", font, (255, 100, 0), HEIGHT // 4)
                hard_message_timer -= 1
                if hard_message_timer <= 0:
                    show_hard_message = False

            pygame.display.flip()

if __name__ == "__main__":
    main()
