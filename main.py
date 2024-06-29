#<---------------MODULES------------------------>
import pygame
import sys
import random
import os


# Class Definitions
class Gun:
    def __init__(self, name, capacity, magazine, bullets, gunposleft_X, gunposleft_Y, flashleft_X, flashleft_Y,
                 gunposright_X, gunposright_Y, flashright_X, flashright_Y):
        self.name = name
        self.magazine = magazine
        self.capacity = capacity
        self.bullets = bullets

        # Guns position on X and Y co-ordinates on Right
        self.gun_RX = gunposright_X
        self.gun_RY = gunposright_Y
        self.flash_RX = flashright_X
        self.flash_RY = flashright_Y

        # Guns position on X and Y co-ordinates on Left
        self.gun_LX = gunposleft_X
        self.gun_LY = gunposleft_Y
        self.flash_LX = flashleft_X
        self.flash_LY = flashleft_Y

        # Guns currentposset
        self.guncur_X = self.gun_LX
        self.guncur_Y = self.gun_LY
        self.flash_X = self.flash_LX
        self.flash_Y = self.flash_LY

    def reload(self):
        if self.bullets == 0:
            return False
        elif self.bullets <= (self.magazine - self.capacity):
            self.capacity += self.bullets
            self.bullets = 0
            return True
        else:
            self.bullets -= (self.magazine - self.capacity)
            self.capacity = self.magazine
            return True

    def shoot(self):
        if self.capacity != 0:
            self.capacity -= 1
            return True
        else:
            self.capacity = 0
            return False

    def isleft(self, pos):
        if pos >= 640:
            self.guncur_X = self.gun_LX
            self.guncur_Y = self.gun_LY
            self.flash_X = self.flash_LX
            self.flash_Y = self.flash_LY
            return "left"
        else:
            self.guncur_X = self.gun_RX
            self.guncur_Y = self.gun_RY
            self.flash_X = self.flash_RX
            self.flash_Y = self.flash_RY
            return "right"

# Class Object for the Life of a player

class Life:
    def __init__(self, value):
        self.value = value

    def onCross(self):
        self.value -= 1

    def onHit(self):
        self.value += 1


class Ghost:
    def __init__(self, addon, curypos, speedx, speedy):
        self.addon = addon
        self.spawn = [200, 1000]
        self.curxpos = random.randrange(200, 1000)
        self.ghostpic = random.randint(0, 4)
        self.curypos = curypos
        self.speedx = speedx
        self.speedy = speedy
        val = random.randint(0, 1)
        if val == 0:
            self.value = "left"
            self.toleft = True
        else:
            self.value = "right"
            self.toleft = False
        self.steps = 5

    def get_pos(self):
        return (self.curxpos, self.curypos)

    def get_type(self):
        return self.ghostpic

    def move(self):
        if self.curxpos >= self.spawn[1]:
            self.toleft = True
            self.value = "left"
        elif self.curxpos <= self.spawn[0]:
            self.toleft = False
            self.value = "right"
        return self.value

    def reuse(self):
        self.ghostpic = random.randint(0, 4)
        self.curxpos = random.randrange(200, 1000)
        self.curypos = 80
        if self.speedx <= 7:
            self.speedx += 0.3
        if self.speedy <= 50 and self.addon in ["Ghost 2", "Ghost 4"]:
            self.speedy += 0.03
        elif self.speedy <= 8:
            self.speedy += 0.03
        val = random.randint(0, 1)
        if val == 0:
            self.value = "left"
            self.toleft = True
        else:
            self.value = "right"
            self.toleft = False
        self.steps = 5

    def zigzag(self):
        if self.toleft:
            self.curxpos -= self.speedx
        else:
            self.curxpos += self.speedx

        self.curypos += self.speedy
        return (self.curxpos, self.curypos)

    def squaremoves(self):
        if self.toleft:
            self.curxpos -= self.speedx
        else:
            self.curxpos += self.speedx
        if self.curxpos >= self.spawn[1] or self.curxpos <= self.spawn[0]:
            self.curypos += self.speedy
        return (self.curxpos, self.curypos)


# __init__ the pygame module
pygame.init()

# High score error fxied 
high_score_file_path = "Gallery/HighScore/highscore.txt"

# Ensure the high score directory exists
os.makedirs(os.path.dirname(high_score_file_path), exist_ok=True)

# Check if the high score file exists, and create it if not
if not os.path.exists(high_score_file_path):
    with open(high_score_file_path, "w") as f:
        f.write("0")

# Open the high score file for reading
with open(high_score_file_path, "r") as f:
    value_ = f.readline()
    high_value = int(value_, 10)

# Load Variables
play = 1
font = pygame.font.Font("Gallery/images/font/digital-7.ttf", 67)
gun_value = 0
score_value = 0

# Frames per seconds
FPS = 120
fpsclock = pygame.time.Clock()

# Screen resolution
width = 1280
height = 760

# Set screen
screen = pygame.display.set_mode((width, height))

# Loading game audio and gallery
Game_gallery = {}
Game_audio = {}

# Load game assets
# BACKGROUND
# Loading Game Backgrounds
Game_gallery["backgrounds"] = (
    pygame.image.load("Gallery/Background/background_1.png").convert_alpha(),
    pygame.image.load("Gallery/Background/background_2.png").convert_alpha(),
    pygame.image.load("Gallery/Background/background_3.png").convert_alpha()
)

# FRAMES
# Gun Display
Game_gallery["display"] = (
    pygame.image.load("Gallery/Frames/Gun Display/P92.png").convert_alpha(),
    pygame.image.load("Gallery/Frames/Gun Display/P1911.png").convert_alpha(),
    pygame.image.load("Gallery/Frames/Gun Display/R1895.png").convert_alpha(),
    pygame.image.load("Gallery/Frames/Gun Display/S1897.png").convert_alpha()
)

# Gun Hold Left
Game_gallery["gun"] = {}
Game_gallery["gun"]["left"] = (
    pygame.image.load("Gallery/Frames/Gun Holding Left/P92.png").convert_alpha(),
    pygame.image.load("Gallery/Frames/Gun Holding Left/P1911.png").convert_alpha(),
    pygame.image.load("Gallery/Frames/Gun Holding Left/R1895.png").convert_alpha(),
    pygame.image.load("Gallery/Frames/Gun Holding Left/S1897.png").convert_alpha()
)

# Gun Hold Right
Game_gallery["gun"]["right"] = (
    pygame.image.load("Gallery/Frames/Gun Holding Right/P92.png").convert_alpha(),
    pygame.image.load("Gallery/Frames/Gun Holding Right/P1911.png").convert_alpha(),
    pygame.image.load("Gallery/Frames/Gun Holding Right/R1895.png").convert_alpha(),
    pygame.image.load("Gallery/Frames/Gun Holding Right/S1897.png").convert_alpha()
)

# IMAGES
# Guns bullets Display
Game_gallery["bullets"] = (
    pygame.image.load("Gallery/images/Bullets/P92.png").convert_alpha(),
    pygame.image.load("Gallery/images/Bullets/P1911.png").convert_alpha(),
    pygame.image.load("Gallery/images/Bullets/R1895.png").convert_alpha(),
    pygame.image.load("Gallery/images/Bullets/S1897.png").convert_alpha()
)

# Magazine images of P92 Gun
Game_gallery["show"] = {}
Game_gallery["show"]["P92"] = (
    pygame.image.load("Gallery/images/clip/P92/ammo 0.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/P92/ammo 1.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/P92/ammo 2.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/P92/ammo 3.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/P92/ammo 4.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/P92/ammo 5.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/P92/ammo 6.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/P92/ammo 7.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/P92/ammo 8.png").convert_alpha()
)

# Magazine images of P1911 Gun
Game_gallery["show"]["P1911"] = (
    pygame.image.load("Gallery/images/clip/P1911/ammo 0.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/P1911/ammo 1.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/P1911/ammo 2.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/P1911/ammo 3.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/P1911/ammo 4.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/P1911/ammo 5.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/P1911/ammo 6.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/P1911/ammo 7.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/P1911/ammo 8.png").convert_alpha()
)

# Magazine images of R1895 Gun
Game_gallery["show"]["R1895"] = (
    pygame.image.load("Gallery/images/clip/R1895/ammo0.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/R1895/ammo1.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/R1895/ammo2.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/R1895/ammo3.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/R1895/ammo4.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/R1895/ammo5.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/R1895/ammo6.png").convert_alpha()
)

# Magazine images of S1897 Gun
Game_gallery["show"]["S1897"] = (
    pygame.image.load("Gallery/images/clip/S1897/ammo 0.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/S1897/ammo 1.png").convert_alpha(),
    pygame.image.load("Gallery/images/clip/S1897/ammo 2.png").convert_alpha()
)

# Flash
Game_gallery["flash"] = (pygame.image.load("Gallery/images/flash/flash.png").convert_alpha())

# Ghosts
Game_gallery["ghost"] = {}
Game_gallery["ghost"]["left"] = (
    pygame.image.load("Gallery/images/Ghosts/Left/ghost (1).png").convert_alpha(),
    pygame.image.load("Gallery/images/Ghosts/Left/ghost (2).png").convert_alpha(),
    pygame.image.load("Gallery/images/Ghosts/Left/ghost (3).png").convert_alpha(),
    pygame.image.load("Gallery/images/Ghosts/Left/ghost (4).png").convert_alpha(),
    pygame.image.load("Gallery/images/Ghosts/Left/ghost (5).png").convert_alpha()
)

Game_gallery["ghost"]["right"] = (
    pygame.image.load("Gallery/images/Ghosts/Right/ghost (1).png").convert_alpha(),
    pygame.image.load("Gallery/images/Ghosts/Right/ghost (2).png").convert_alpha(),
    pygame.image.load("Gallery/images/Ghosts/Right/ghost (3).png").convert_alpha(),
    pygame.image.load("Gallery/images/Ghosts/Right/ghost (4).png").convert_alpha(),
    pygame.image.load("Gallery/images/Ghosts/Right/ghost (5).png").convert_alpha()
)

# CrossHair
Game_gallery["crosshair"] = (
    pygame.image.load("Gallery/images/crosshair1.png").convert_alpha(),
    pygame.image.load("Gallery/images/crosshair2.png").convert_alpha()
)

# Health
Game_gallery["health"] = (pygame.image.load("Gallery/images/health.png").convert_alpha())

# Pause and play button
Game_gallery["pause_play"] = (pygame.image.load("Gallery/images/play-button.png").convert_alpha())

# GAME AUDIO
# Background music
Game_audio["music"] = (
    pygame.mixer.Sound("Gallery/Sounds/Songs/Song.mp3")
)

# Empty lock of guns
Game_audio["empty"] = (
    pygame.mixer.Sound("Gallery/Sounds/gun 1/empty.mp3"),
    pygame.mixer.Sound("Gallery/Sounds/gun 2/empty.mp3"),
    pygame.mixer.Sound("Gallery/Sounds/gun 3/empty.mp3"),
    pygame.mixer.Sound("Gallery/Sounds/gun 4/empty.mp3")
)

# Reload lock of guns
Game_audio["reload"] = (
    pygame.mixer.Sound("Gallery/Sounds/gun 1/reload.mp3"),
    pygame.mixer.Sound("Gallery/Sounds/gun 2/reload.mp3"),
    pygame.mixer.Sound("Gallery/Sounds/gun 3/reload.mp3"),
    pygame.mixer.Sound("Gallery/Sounds/gun 4/reload.mp3")
)

# Shoot lock of guns
Game_audio["shoot"] = (
    pygame.mixer.Sound("Gallery/Sounds/gun 1/shoot.mp3"),
    pygame.mixer.Sound("Gallery/Sounds/gun 2/shoot.mp3"),
    pygame.mixer.Sound("Gallery/Sounds/gun 3/shoot.mp3"),
    pygame.mixer.Sound("Gallery/Sounds/gun 4/shoot.mp3")
)

# Creating Ghosts Objects
ghost1 = Ghost("Ghost 1", 80, 1, 0.5)
ghost2 = Ghost("Ghost 2", 80, 4, 20)
ghost3 = Ghost("Ghost 3", 80, 3, 0.5)
ghost4 = Ghost("Ghost 4", 80, 2, 30)
ghost5 = Ghost("Ghost 5", 80, 2.1, 0.5)
Ghost_list = [ghost1, ghost2, ghost3, ghost4, ghost5]

# Creating Gun Objects
S1897 = Gun("S1897", 2, 2, 10, 0, 533, 250, 430, 880, 532, 805, 430)
P92 = Gun("P92", 8, 8, 24, 110, 518, 215, 435, 870, 518, 840, 435)
P1911 = Gun("P1911", 8, 8, 30, 110, 501, 215, 420, 870, 501, 840, 420)
R1895 = Gun("R1895", 6, 6, 18, 80, 503, 225, 420, 900, 503, 830, 420)

# Creating Life Objects
LIFE = Life(3)
guncollection = [P92, P1911, R1895, S1897]
__inuse__ = guncollection[gun_value]

Game_audio["music"].play(-1)

while True:
    screen.blit(Game_gallery["backgrounds"][1], (0, 0))
    position = pygame.mouse.get_pos()
    __inuse__ = guncollection[gun_value]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                play = (play + 1) % 2

        if event.type == pygame.MOUSEBUTTONDOWN:
            if play == 3:
                if event.button == 3:
                    for ghost in Ghost_list:
                        ghost.reuse()
                    for gun in guncollection:
                        gun.bullets = 24 if gun.name == "P92" else 30 if gun.name == "P1911" else 18 if gun.name == "R1895" else 10
                        gun.capacity = gun.magazine
                    LIFE.value = 3
                    play = 1
                    score_value = 0
                    gun_value = 0

            if play == 1:
                if event.button == 1:
                    if 10 <= position[0] <= 60 and 10 <= position[1] <= 60:
                        play = (play + 1) % 2
                    else:
                        if __inuse__.shoot():
                            screen.blit(Game_gallery["flash"], (__inuse__.flash_X, __inuse__.flash_Y))
                            Game_audio["shoot"][gun_value].play()
                            for ghost in Ghost_list:
                                coord = ghost.get_pos()
                                if coord[0] < position[0] < coord[0] + 100 and coord[1] < position[1] < coord[1] + 100:
                                    score_value += 5
                                    if ghost.get_type() == 4:
                                        __inuse__.bullets += 3
                                    ghost.reuse()
                        else:
                            Game_audio["empty"][gun_value].play()

                if event.button == 3:
                    if __inuse__.reload():
                        Game_audio["reload"][gun_value].play()
                    else:
                        Game_audio["empty"][gun_value].play()

                if event.button == 4:
                    gun_value = (gun_value + 1) % 4
                if event.button == 5:
                    gun_value = (gun_value - 1) % 4

            else:
                if event.button == 1 and play != 3:
                    if 10 <= position[0] <= 60 and 10 <= position[0] <= 60:
                        play = (play + 1) % 2

    if play != 3:
        screen.blit(Game_gallery["pause_play"], (10, 10))

    if play == 1:
        pygame.mouse.set_visible(False)
        count_ = 0
        for gh in Ghost_list:
            count_ += 1
            if count_ % 2 == 0:
                screen.blit(Game_gallery["ghost"][gh.move()][gh.ghostpic], gh.squaremoves())
            else:
                screen.blit(Game_gallery["ghost"][gh.move()][gh.ghostpic], gh.zigzag())

            if gh.curypos > 670:
                LIFE.value -= 1
                gh.curypos = 80
        if LIFE.value <= 0:
            play = 3
        if LIFE.value >= 1:
            screen.blit(Game_gallery["health"], (1200, 10))
        if LIFE.value >= 2:
            screen.blit(Game_gallery["health"], (1130, 10))
        if LIFE.value >= 3:
            screen.blit(Game_gallery["health"], (1060, 10))
        screen.blit(Game_gallery["display"][gun_value], (10, 100))
        screen.blit(Game_gallery["bullets"][gun_value], (10, 180))
        screen.blit(font.render(f"x {__inuse__.bullets}", True, (0, 255, 0)), (70, 180))
        screen.blit(Game_gallery["show"][__inuse__.name][__inuse__.capacity], (1160, 100))

        screen.blit(Game_gallery["gun"][__inuse__.isleft(position[0])][gun_value],
                    (__inuse__.guncur_X, __inuse__.guncur_Y))
        screen.blit(font.render(f"SCORE: {score_value}", True, (255, 255, 255)), (500, 10))

        if gun_value != 3:
            screen.blit(Game_gallery["crosshair"][0], (position[0] - 25, position[1] - 25))
        else:
            screen.blit(Game_gallery["crosshair"][1], (position[0] - 25, position[1] - 25))

    elif play == 3:
        pygame.mouse.set_visible(True)
        screen.blit(font.render("GAME OVER", True, (255, 0, 0)), (510, 250))
        screen.blit(font.render("RIGHT CLICK TO RESTART", True, (0, 0, 0)), (340, 330))
        if score_value > high_value:
            high_value = score_value
            with open(high_score_file_path, "w") as f:
                f.write(f"{high_value}")
        screen.blit(font.render(f"YOUR SCORE: {score_value}", True, (0, 0, 0)), (450, 410))
        screen.blit(font.render(f"HIGH SCORE: {high_value}", True, (0, 0, 0)), (460, 490))
    else:
        pygame.mouse.set_visible(True)
        screen.blit(font.render("PAUSED!", True, (255, 255, 255)), (500, 300))

    pygame.display.update()
    fpsclock.tick(FPS)
