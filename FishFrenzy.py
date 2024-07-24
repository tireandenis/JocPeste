import pygame
from os.path import join
from random import randint, uniform

# setup
pygame.display.set_caption("Fish Frenzy")
pygame.init()
screen_lungime, screen_latime = 1270, 720
display_surface = pygame.display.set_mode((screen_lungime, screen_latime))
clock = pygame.time.Clock()

# scor initial
score_plus = 0

# Font
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)
menu_font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 60)

# images
pestemic_surf = pygame.image.load(join('images', 'Fish Png1.png')).convert_alpha()
pestemij_surf = pygame.image.load(join("images", "fish3Texture.png")).convert_alpha()
pestemare_surf = pygame.image.load(join("images", "fish4Texture.png")).convert_alpha()
player_surf = pygame.image.load(join('images', 'PesteDreapta.png')).convert_alpha()
player_surf_Left = pygame.image.load(join('images', 'PesteStanga.png')).convert_alpha()
papa_animation = pygame.image.load(join("images", "PestePapa1.png")).convert_alpha()
bg = pygame.image.load(join("images", "background1.png"))

# Create flipped and scaled images
pestemic_surf_oglinda = pygame.transform.flip(pestemic_surf, True, False)
pestemij_surf_oglinda = pygame.transform.flip(pestemij_surf, True, False)
pestemare_surf_oglinda = pygame.transform.flip(pestemare_surf, True, False)
papa_animation_oglinda = pygame.transform.flip(papa_animation, True, False)
bg_scale = pygame.transform.scale(bg, (screen_lungime, screen_latime))

# Game states
MENU, GAME, GAME_OVER = "menu", "game", "game_over"
game_state = MENU


# Sprites
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = player_surf
        self.image_left = player_surf_Left
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(screen_lungime / 2, screen_latime / 2))
        self.direction = pygame.Vector2()
        self.speed = 500
        self.marime = 1
        self.spre_dreapta = True
        self.image_cache = {}
        self.mananca = False
        self.timp_mananca = 0

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if not self.mananca:
            self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
            self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
            self.direction = self.direction.normalize() if self.direction else self.direction
            self.rect.center += self.direction * self.speed * dt

            if keys[pygame.K_LEFT]:
                self.spre_dreapta = False
            elif keys[pygame.K_RIGHT]:
                self.spre_dreapta = True

            self.update_image()

            # Dash
            if keys[pygame.K_SPACE]:
                self.speed = 750
            else:
                self.speed = 500

        else:
            self.timp_mananca -= dt
            if self.timp_mananca <= 0:
                self.mananca = False
                self.update_image()

        self.update_image()

    def update_image(self):
        if self.mananca:
            if self.spre_dreapta:
                self.image = pygame.transform.scale(papa_animation, (
                    int(self.original_image.get_width() * self.marime),
                    int(self.original_image.get_height() * self.marime)
                ))
            else:
                self.image = pygame.transform.scale(papa_animation_oglinda, (
                    int(self.original_image.get_width() * self.marime),
                    int(self.original_image.get_height() * self.marime)
                ))
        else:
            direction = 'right' if self.spre_dreapta else 'left'
            if (direction, self.marime) in self.image_cache:
                self.image = self.image_cache[(direction, self.marime)]
            else:
                if self.spre_dreapta:
                    self.image = pygame.transform.scale(self.original_image, (
                        int(self.original_image.get_width() * self.marime),
                        int(self.original_image.get_height() * self.marime)))
                else:
                    self.image = pygame.transform.scale(self.image_left, (
                        int(self.image_left.get_width() * self.marime),
                        int(self.image_left.get_height() * self.marime)))
                self.image_cache[(direction, self.marime)] = self.image

            self.rect = self.image.get_rect(center=self.rect.center)
            self.mask = pygame.mask.from_surface(self.image)

    def Creste(self):
        self.marime += 0.02
        self.update_image()

    def Papa(self):
        self.mananca = True
        self.timp_mananca = 0.1
        self.update_image()


class PesteMic(pygame.sprite.Sprite):
    def __init__(self, surf, pos, speed, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed

    def update(self, dt):
        self.rect.centerx += self.speed * dt
        if self.rect.right < 0 or self.rect.left > screen_lungime:
            self.kill()


class PesteMij(pygame.sprite.Sprite):
    def __init__(self, surf, pos, speed, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed

    def update(self, dt):
        self.rect.centerx += self.speed * dt
        if self.rect.right < 0 or self.rect.left > screen_lungime:
            self.kill()


class PesteMare(pygame.sprite.Sprite):
    def __init__(self, surf, pos, speed, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed

    def update(self, dt):
        self.rect.centerx += self.speed * dt
        if self.rect.right < 0 or self.rect.left > screen_lungime:
            self.kill()


# Events
pestemic_event = pygame.event.custom_type()
pygame.time.set_timer(pestemic_event, int(uniform(900, 1100)))

pestemij_event = pygame.event.custom_type()
pygame.time.set_timer(pestemij_event, int(uniform(10000, 14000)))

pestemare_event = pygame.event.custom_type()
pygame.time.set_timer(pestemare_event, int(uniform(18000, 22000)))

all_sprites = pygame.sprite.Group()
player = Player(all_sprites)
pestemic_sprites = pygame.sprite.Group()
pestemij_sprites = pygame.sprite.Group()
pestemare_sprites = pygame.sprite.Group()


def score():
    score_surf = font.render(str(score_plus), True, "white")
    score_rect = score_surf.get_rect(midtop=(screen_lungime / 2, 10))
    display_surface.blit(score_surf, score_rect)


def collisions():
    global score_plus
    global game_state

    papa_mic = pygame.sprite.spritecollide(player, pestemic_sprites, True, pygame.sprite.collide_mask)
    papa_mij = pygame.sprite.spritecollide(player, pestemij_sprites, True, pygame.sprite.collide_mask)
    papa_mare = pygame.sprite.spritecollide(player, pestemare_sprites, True, pygame.sprite.collide_mask)
    if papa_mic:
        score_plus += 1
        player.Creste()
        player.Papa()

    if papa_mij and score_plus < 10:
        game_state = GAME_OVER
    elif papa_mij:
        score_plus += 2
        player.Creste()
        player.Papa()

    if papa_mare and score_plus < 15:
        game_state = GAME_OVER
    elif papa_mare:
        score_plus += 5
        player.Creste()
        player.Papa()


def draw_main_menu():
    display_surface.blit(bg_scale, (0, 0))
    title_surf = menu_font.render("Fish Frenzy", True, "white")
    start_surf = font.render("Press SPACE to Start", True, "white")
    quit_surf = font.render("Press Q to Quit", True, "white")

    title_rect = title_surf.get_rect(center=(screen_lungime / 2, screen_latime / 3))
    start_rect = start_surf.get_rect(center=(screen_lungime / 2, screen_latime / 2))
    quit_rect = quit_surf.get_rect(center=(screen_lungime / 2, screen_latime / 2 + 100))

    display_surface.blit(title_surf, title_rect)
    display_surface.blit(start_surf, start_rect)
    display_surface.blit(quit_surf, quit_rect)

    pygame.display.update()


def draw_game_over():
    display_surface.blit(bg_scale, (0, 0))
    game_over_surf = menu_font.render("Game Over", True, "white")
    restart_surf = font.render("Press R to Restart", True, "white")
    quit_surf = font.render("Press Q to Quit", True, "white")

    game_over_rect = game_over_surf.get_rect(center=(screen_lungime / 2, screen_latime / 3))
    restart_rect = restart_surf.get_rect(center=(screen_lungime / 2, screen_latime / 2))
    quit_rect = quit_surf.get_rect(center=(screen_lungime / 2, screen_latime / 2 + 100))

    display_surface.blit(game_over_surf, game_over_rect)
    display_surface.blit(restart_surf, restart_rect)
    display_surface.blit(quit_surf, quit_rect)

    pygame.display.update()


running = True
while running:
    dt = clock.tick(60) / 1000  # limits FPS to 60

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = GAME
                if event.key == pygame.K_q:
                    running = False
        elif game_state == GAME:
            if event.type == pestemic_event:
                x, y = randint(screen_lungime, screen_lungime), randint(20, screen_latime)
                PesteMic(pestemic_surf, (x, y), -100, (all_sprites, pestemic_sprites))
                x, y = randint(0, 0), randint(15, screen_latime)
                PesteMic(pestemic_surf_oglinda, (x, y), 100, (all_sprites, pestemic_sprites))

            if event.type == pestemij_event:
                x, y = randint(screen_lungime, screen_lungime), randint(20, screen_latime)
                PesteMij(pestemij_surf_oglinda, (x, y), -75, (all_sprites, pestemij_sprites))
                x, y = randint(0, 0), randint(15, screen_latime)
                PesteMij(pestemij_surf, (x, y), 75, (all_sprites, pestemij_sprites))

            if event.type == pestemare_event:
                x, y = randint(screen_lungime, screen_lungime), randint(20, screen_latime)
                PesteMare(pestemare_surf_oglinda, (x, y), -50, (all_sprites, pestemare_sprites))
                x, y = randint(0, 0), randint(15, screen_latime)
                PesteMare(pestemare_surf, (x, y), 50, (all_sprites, pestemare_sprites))
        elif game_state == GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_state = GAME
                    score_plus = 0
                    all_sprites.empty()
                    player = Player(all_sprites)
                if event.key == pygame.K_q:
                    running = False

    if game_state == MENU:
        draw_main_menu()
    elif game_state == GAME:
        all_sprites.update(dt)
        collisions()

        display_surface.blit(bg_scale, (0, 0))
        score()
        all_sprites.draw(display_surface)
        pygame.display.update()
    elif game_state == GAME_OVER:
        draw_game_over()

pygame.quit()
