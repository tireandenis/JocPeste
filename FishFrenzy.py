import pygame
from os.path import join
from random import randint, uniform

# setup
pygame.display.set_caption("Fish Frenzy")
pygame.init()
screen_lungime, screen_latime = 1270, 720
display_surface = pygame.display.set_mode((screen_lungime, screen_latime), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Font
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)
menu_font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 60)

# images
boss_surf = pygame.image.load(join("images", "Shark.gif"))
pestemic_surf = pygame.image.load(join('images', 'Fish Png1.png')).convert_alpha()
pestemij_surf = pygame.image.load(join("images", "fish3Texture.png")).convert_alpha()
pestemare_surf = pygame.image.load(join("images", "fish4Texture.png")).convert_alpha()
player_surf = pygame.image.load(join('images', 'PesteDreapta.png')).convert_alpha()
player_surf_Left = pygame.image.load(join('images', 'PesteStanga.png')).convert_alpha()
papa_animation = pygame.image.load(join("images", "PestePapa1.png")).convert_alpha()
bg = pygame.image.load(join("images", "background1.png"))

# Create flipped and scaled images
boss_scale = pygame.transform.scale(boss_surf, (200, 160))
pestemij_scale = pygame.transform.scale(pestemij_surf, (85, 75))
pestemare_scale = pygame.transform.scale(pestemare_surf, (140, 80))
pestemic_surf_oglinda = pygame.transform.flip(pestemic_surf, True, False)
pestemij_surf_oglinda = pygame.transform.flip(pestemij_scale, True, False)
pestemare_surf_oglinda = pygame.transform.flip(pestemare_scale, True, False)
papa_animation_oglinda = pygame.transform.flip(papa_animation, True, False)
boss_oglinda = pygame.transform.flip(boss_scale, True, False)
bg_scale = pygame.transform.scale(bg, (screen_lungime, screen_latime))

#Game SFX

papa_sfx = pygame.mixer.Sound(join("sfx", "eating-sound-effect-36186.mp3"))
game_music = pygame.mixer.Sound(join("sfx", "main-theme-68815.mp3"))
game_over_sfx = pygame.mixer.Sound(join("sfx", "game-over-arcade-6435.mp3"))
game_win = pygame.mixer.Sound(join("sfx", "success-fanfare-trumpets-6185.mp3"))




# Game states
MENU, GAME, GAME_OVER, PAUSE, WIN = "menu", "game", "game_over", "pause", "victory"


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

    def creste(self, increment):
        self.marime += increment
        self.update_image()

    def papa(self):
        self.mananca = True
        self.timp_mananca = 0.05
        self.update_image()
        papa_sfx.play()

class Boss(pygame.sprite.Sprite):
    def __init__(self, surf, pos, speed, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.direction = pygame.Vector2(3, 2).normalize()

    def update(self, dt):
        if self.rect.bottom > screen_latime or self.rect.top < 0:
            self.direction.y *= -1
        if self.rect.right > 1300:
            self.image = boss_scale
            self.direction.x *= -1

        if self.rect.left < 0:
            self.image = boss_oglinda
            self.direction.x *= -1

        self.rect.center -= self.direction * self.speed * dt
        if self.rect.right < 0 or self.rect.left > screen_lungime or self.rect.bottom < 0 or self.rect.top > screen_latime:
            self.kill()

        for group in [game.pestemic_sprites, game.pestemij_sprites, game.pestemare_sprites]:
            for fish in pygame.sprite.spritecollide(self, group, True, pygame.sprite.collide_mask):

                fish.kill()





class Peste(pygame.sprite.Sprite):
    def __init__(self, surf, pos, speed, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed

    def update(self, dt):
        self.rect.centerx += self.speed * dt
        if self.rect.right < 0 or self.rect.left > screen_lungime:
            self.kill()


class PesteMic(Peste):
    def __init__(self, surf, pos, speed, groups):
        super().__init__(surf, pos, speed, groups)


class PesteMij(Peste):
    def __init__(self, surf, pos, speed, groups):
        super().__init__(surf, pos, speed, groups)


class PesteMare(Peste):
    def __init__(self, surf, pos, speed, groups):
        super().__init__(surf, pos, speed, groups)







class FishFrenzyGame:

    def __init__(self):
        game_music.play(-1)
        self.game_state = MENU
        self.score_plus = 0
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self.all_sprites)
        self.pestemic_sprites = pygame.sprite.Group()
        self.pestemij_sprites = pygame.sprite.Group()
        self.pestemare_sprites = pygame.sprite.Group()
        self.boss_sprites = pygame.sprite.Group()
        self.boss_spawn = False
        self.boss_spawned = False  # Flag to track boss spawn

        # Events
        self.pestemic_event = pygame.event.custom_type()
        pygame.time.set_timer(self.pestemic_event, int(uniform(1000, 2000)))

        self.pestemij_event = pygame.event.custom_type()
        pygame.time.set_timer(self.pestemij_event, int(uniform(4000, 6000)))

        self.pestemare_event = pygame.event.custom_type()
        pygame.time.set_timer(self.pestemare_event, int(uniform(10000, 12000)))

        self.boss_event = pygame.event.custom_type()
        pygame.time.set_timer(self.boss_event, int(uniform(1000, 1500)))





    def score(self):
        score_surf = font.render(str(self.score_plus), True, "white")
        score_rect = score_surf.get_rect(midtop=(screen_lungime / 2, 10))
        display_surface.blit(score_surf, score_rect)

    def collisions(self):
        papa_mic = pygame.sprite.spritecollide(self.player, self.pestemic_sprites, True, pygame.sprite.collide_mask)
        papa_mij = pygame.sprite.spritecollide(self.player, self.pestemij_sprites, True, pygame.sprite.collide_mask)
        papa_mare = pygame.sprite.spritecollide(self.player, self.pestemare_sprites, True, pygame.sprite.collide_mask)
        papa_boss = pygame.sprite.spritecollide(self.player, self.boss_sprites, True, pygame.sprite.collide_mask)

        if papa_mic:
            self.score_plus += 1
            self.player.creste(0.01)
            self.player.papa()

        if papa_mij and self.score_plus < 50:
            self.game_state = GAME_OVER
            game_over_sfx.play()
        elif papa_mij:
            self.score_plus += 2
            self.player.creste(0.03)
            self.player.papa()

        if papa_mare and self.score_plus < 80:
            self.game_state = GAME_OVER
            game_over_sfx.play()
        elif papa_mare:
            self.score_plus += 5
            self.player.creste(0.06)
            self.player.papa()

        if papa_boss and self.score_plus < 150:
            self.game_state = GAME_OVER
            game_over_sfx.play()

        elif papa_boss:
            self.game_state = WIN
            game_win.play()





    def draw_main_menu(self):
        display_surface.blit(bg_scale, (0, 0))
        title_surf = menu_font.render("Fish Frenzy", True, "blue")
        start_surf = font.render("Press SPACE to Start", True, "green")
        quit_surf = font.render("Press Q to Quit", True, "red")

        title_rect = title_surf.get_rect(center=(screen_lungime / 2, screen_latime / 3))
        start_rect = start_surf.get_rect(center=(screen_lungime / 2, screen_latime / 2))
        quit_rect = quit_surf.get_rect(center=(screen_lungime / 2, screen_latime / 2 + 100))

        display_surface.blit(title_surf, title_rect)
        display_surface.blit(start_surf, start_rect)
        display_surface.blit(quit_surf, quit_rect)

        pygame.display.update()

    def draw_game_over(self):
        display_surface.blit(bg_scale, (0, 0))
        game_over_surf = menu_font.render("Game Over", True, "red")
        restart_surf = font.render("Press R to Restart", True, "yellow")
        quit_surf = font.render("Press Q to Quit", True, "red")

        game_over_rect = game_over_surf.get_rect(center=(screen_lungime / 2, screen_latime / 3))
        restart_rect = restart_surf.get_rect(center=(screen_lungime / 2, screen_latime / 2))
        quit_rect = quit_surf.get_rect(center=(screen_lungime / 2, screen_latime / 2 + 100))

        display_surface.blit(game_over_surf, game_over_rect)
        display_surface.blit(restart_surf, restart_rect)
        display_surface.blit(quit_surf, quit_rect)

        pygame.display.update()

    def draw_pause(self):
        #PRESS P TO PAUSE
        display_surface.blit(bg_scale, (0, 0))
        pause_surf = menu_font.render("The Game Is Paused", True, "white")
        unpause_surf = menu_font.render("Press P to Resume", True, "white")
        restart_surf = font.render("Press R to Restart", True, "yellow")

        pause_rect = pause_surf.get_rect(center=(screen_lungime / 2, screen_latime / 3))
        restart_rect = restart_surf.get_rect(center=(screen_lungime / 2, screen_latime / 2 + 100))
        unpause_rect = unpause_surf.get_rect(center=(screen_lungime / 2, screen_latime / 2))

        display_surface.blit(pause_surf, pause_rect)
        display_surface.blit(restart_surf, restart_rect)
        display_surface.blit(unpause_surf, unpause_rect)

        pygame.display.update()

    def draw_win(self):
        display_surface.blit(bg_scale, (0, 0))
        win_surf = menu_font.render("Congratulations, you won !!!", True, "green")
        restart_surf = font.render("Press R to Restart", True, "yellow")

        win_rect = win_surf.get_rect(center=(screen_lungime / 2, screen_latime / 3))
        restart_rect = restart_surf.get_rect(center=(screen_lungime / 2, screen_latime / 2 + 100))

        display_surface.blit(win_surf, win_rect)
        display_surface.blit(restart_surf, restart_rect)

        pygame.display.update()





    def reset_game(self):
        self.score_plus = 0
        self.all_sprites.empty()
        self.player = Player(self.all_sprites)
        self.pestemic_sprites.empty()
        self.pestemij_sprites.empty()
        self.pestemare_sprites.empty()
        self.boss_sprites.empty()

    def run(self):
        running = True
        while running:
            dt = clock.tick(60) / 1000  # limits FPS to 60

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.game_state == MENU:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.game_state = GAME
                        if event.key == pygame.K_q:
                            running = False
                elif self.game_state == GAME:


                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.game_state = PAUSE


                    if event.type == self.pestemic_event:
                        x, y = randint(screen_lungime, screen_lungime), randint(10, screen_latime)
                        PesteMic(pestemic_surf, (x, y), -100, (self.all_sprites, self.pestemic_sprites))
                        x, y = randint(0, 0), randint(-10, screen_latime)
                        PesteMic(pestemic_surf_oglinda, (x, y), 100, (self.all_sprites, self.pestemic_sprites))

                    if event.type == self.pestemij_event:
                        x, y = randint(screen_lungime, screen_lungime), randint(20, screen_latime)
                        PesteMij(pestemij_surf_oglinda, (x, y), -80, (self.all_sprites, self.pestemij_sprites))
                        x, y = randint(0, 0), randint(15, screen_latime)
                        PesteMij(pestemij_scale, (x, y), 80, (self.all_sprites, self.pestemij_sprites))

                    if event.type == self.pestemare_event:
                        x, y = randint(screen_lungime, screen_lungime), randint(20, screen_latime)
                        PesteMare(pestemare_surf_oglinda, (x, y), -80, (self.all_sprites, self.pestemare_sprites))
                        x, y = randint(0, 0), randint(15, screen_latime)
                        PesteMare(pestemare_scale, (x, y), 80, (self.all_sprites, self.pestemare_sprites))

                    if event.type == self.boss_event and not self.boss_spawned:
                        if self.score_plus >= 50:
                            self.boss_spawned = True
                            x, y = 1200, 360
                            Boss(boss_scale, (x, y), 400, (self.all_sprites, self.boss_sprites))






                elif self.game_state == GAME_OVER:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.reset_game()
                            self.game_state = GAME
                        if event.key == pygame.K_q:
                            running = False


                elif self.game_state == PAUSE:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.game_state = GAME

                        if event.key == pygame.K_r:
                            self.reset_game()
                            self.game_state = GAME

                        if event.key == pygame.K_q:
                            running = False
                elif self.game_state == WIN:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.reset_game()
                            self.game_state = GAME



            if self.game_state == MENU:
                self.draw_main_menu()

            elif self.game_state == GAME:
                self.all_sprites.update(dt)
                self.collisions()



                display_surface.blit(bg_scale, (0, 0))
                self.score()
                self.all_sprites.draw(display_surface)
                pygame.display.update()




            elif self.game_state == PAUSE:
                self.draw_pause()

            elif self.game_state == GAME_OVER:

                self.draw_game_over()

            elif self.game_state == WIN:
                self.draw_win()

        pygame.quit()


# Start the game
if __name__ == "__main__":
    game = FishFrenzyGame()
    game.run()
