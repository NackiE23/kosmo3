import os
import random
import pygame
from live import Live
from stats import Stats


pygame.font.init()
pygame.mixer.init()
# pygame.mixer.music.load('assets/music/Dragon-Castle.mp3')
# pygame.mixer.music.play(-1)
# Dragon Castle by Makai Symphony | https://soundcloud.com/makai-symphony
# Music promoted by https://www.chosic.com/free-music/all/
# Creative Commons CC BY-SA 3.0
# https://creativecommons.org/licenses/by-sa/3.0/

# !!!THE BEST!!!
# pygame.mixer.music.load('assets/music/Saga-of-Knight.mp3')
# pygame.mixer.music.play(-1)
# Saga of Knight  by Makai
# Symphony | https: // soundcloud.com / makai - symphony
# Music promoted by https: // www.chosic.com / free - music / all /
# Creative Commons CC BY - SA 3.0 https: // creativecommons.org / licenses / by - sa / 3.0 /

# pygame.mixer.music.load('assets/music/alexander-nakarada-the-great-battle.mp3')
# pygame.mixer.music.play(-1)
#  The Great Battle by Alexander Nakarada | https://www.serpentsoundstudios.com
# Attribution 4.0 International (CC BY 4.0)
# https://creativecommons.org/licenses/by/4.0/
# Music promoted by https://www.chosic.com/free-music/all/

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kosmo 3.0")

# Load Images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets/images", "kosmo_small_red_villain.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets/images", "kosmo_small_green_villain.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets/images", "kosmo_small_blue_villain.png"))
FIRST_BOSS = pygame.image.load(os.path.join("assets/images", "kosmo_boss_1.png"))
SECOND_BOSS = pygame.image.load(os.path.join("assets/images", "kosmo_boss_2.png"))

# Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets/images", "kosmo_big_super_gun.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets/images", "kosmo_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets/images", "kosmo_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets/images", "kosmo_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets/images", "kosmo_laser_bullet.png"))
BOSS_BULLET = pygame.image.load(os.path.join("assets/images", "kosmo_boss_bullet.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "kosmo_background.png")), (WIDTH, HEIGHT))


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y < height and self.y + 100 >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 7

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj, hit):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= hit
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + self.ship_img.get_width()/2, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    numbers_of_dead = 0

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs, hit):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        if obj.health - hit <= 0:
                            self.numbers_of_dead += 1
                            objs.remove(obj)
                        else:
                            obj.health -= hit
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10,
                          self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10,
                          self.ship_img.get_width() * (self.health/self.max_health), 10))


class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                }

    def __init__(self, x, y, color, health=25):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class Boss(Ship):
    BOSS_COLOR = {"blue": (FIRST_BOSS, BOSS_BULLET),
                  "purple": (SECOND_BOSS, BOSS_BULLET)}

    def __init__(self, x, y, color, health=1000):
        super().__init__(x, y, health)
        self.max_health = health
        self.ship_img, self.laser_img = self.BOSS_COLOR[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y + self.ship_img.get_height() - 30, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def shoot1(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + 20, self.y + self.ship_img.get_height() - 30, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def shoot2(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + 80, self.y + self.ship_img.get_height() - 30, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x, self.y - self.ship_img.get_height() / 4,
                          self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0),
                         (self.x, self.y - self.ship_img.get_height() / 4,
                          self.ship_img.get_width() * (self.health/self.max_health), 10))


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def main():
    pygame.mixer.music.load('assets/music/Saga-of-Knight.mp3')
    pygame.mixer.music.play(-1)
    run, pause = True, False
    fps = 60
    level = 0
    lives = 3
    live = Live(WIN, lives)
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    # waves
    enemies = []
    wave_length = 2
    wave_length_plus = 3
    boss_wave = 0

    # hits
    enemy_hit = 10
    boss_hit = 34
    player_hit = 25

    # movements
    enemy_vel = 2.7
    enemy_vel_plus = .3
    player_vel = 10
    laser_vel = 20
    boss_vel = .5

    player = Player(300, 630)

    clock = pygame.time.Clock()
    stats = Stats(level, player_vel, player_hit, player.numbers_of_dead)

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        score_label = main_font.render(f"Wave: {level}", True, (255, 255, 255))

        WIN.blit(score_label, (WIDTH - score_label.get_width() - 10, 10))
        live.draw()
        stats.level = level
        stats.player_vel = player_vel
        stats.power = player_hit
        stats.numbers_of_dead = player.numbers_of_dead
        stats.draw(WIN, HEIGHT)

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            pygame.mixer.music.unload()
            lost_lable = lost_font.render("YOU LOST!!!", True, (255, 255, 255))
            WIN.blit(lost_lable, (WIDTH/2 - lost_lable.get_width()/2, 350))

        pygame.display.update()

    def pause():
        paused = True
        pygame.mixer.music.pause()
        
        while paused:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE or ev.key == pygame.K_SPACE:
                        pygame.mixer.music.unpause()
                        paused = False
                    if ev.key == pygame.K_q:
                        pygame.quit()
                        quit()

            pause_lable = main_font.render("PAUSE", True, (255, 255, 255))
            WIN.blit(pause_lable, (WIDTH/2 - pause_lable.get_width()/2, HEIGHT/2 - pause_lable.get_height()/2))
            pygame.display.update()
            clock.tick(5)

    while run:
        clock.tick(fps)
        redraw_window()

        if player.health <= 0:
            lives -= 1
            live.amount -= 1
            player.health = 100

        if lives <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > fps * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            if level == 100:
                b, wave_length = wave_length, 300
                for i in range(wave_length):
                    # appearence enemies
                    enemy = Enemy(random.randrange(50, WIDTH - 100),
                                  random.randrange(-1500, -100),
                                  random.choice(["red", "blue", "green"]))
                    enemies.append(enemy)
                wave_length = b
            elif level % 5 == 0:
                boss_wave += 1
                if boss_wave == 1:
                    enemy = Boss(random.randrange(50, WIDTH - 150), -100, "purple", health=800)
                    enemies.append(enemy)
                elif boss_wave == 2:
                    enemy = Boss(random.randrange(50, WIDTH - 150), -100, "blue", health=1200)
                    enemies.append(enemy)
            else:
                enemy_vel += enemy_vel_plus
                wave_length += wave_length_plus
                for i in range(wave_length):
                    # appearence enemies
                    enemy = Enemy(random.randrange(50, WIDTH-100),
                                  random.randrange(-1500, -100),
                                  random.choice(["red", "blue", "green"]))
                    enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        if keys[pygame.K_ESCAPE]:
            pause()
        if keys[pygame.K_z]:
            player_vel += 1
        if keys[pygame.K_x]:
            if player_vel == 0:
                pass
            else:
                player_vel -= 1

        # ENEMIES/BOSSES WAVES
        if level % 5 == 0:
            for enemy in enemies:
                enemy.move(boss_vel)
                enemy.move_lasers(laser_vel, player, boss_hit)

                if random.randrange(0, 60) == 1:
                    enemy.shoot()
                if random.randrange(0, 60) == 1:
                    enemy.shoot1()
                if random.randrange(0, 60) == 1:
                    enemy.shoot2()

                if collide(enemy, player):
                    player.health -= boss_hit
                    enemies.remove(enemy)
                elif enemy.y + enemy.get_height() > HEIGHT:
                    lives -= 1
                    live.amount -= 1
                    enemies.remove(enemy)
        else:
            for enemy in enemies:
                enemy.move(enemy_vel)
                enemy.move_lasers(laser_vel, player, enemy_hit)

                if random.randrange(0, 2*60) == 1:
                    enemy.shoot()

                if collide(enemy, player):
                    player.health -= enemy_hit
                    enemies.remove(enemy)
                elif enemy.y + enemy.get_height() > HEIGHT:
                    lives -= 1
                    live.amount -= 1
                    enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies, player_hit)


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press any key to begin....", True, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


if __name__ == "__main__":
    main_menu()
