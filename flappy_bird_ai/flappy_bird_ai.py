import pygame
import neat
import time
import os
import random

# os window size
WIN_WIDTH = 500
WIN_HEIGHT = 800

# game images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs/bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs/bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs/bird3.png")))]
PIPE_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs/pipe.png")))]
BG_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs/bg.png")))]
BASE_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs/base.png")))]


# object classes
class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25  # tilt bird up, down 25 degrees
    ROT_VEL = 20  # how much to rotate on each frame
    ANIMATION_TIME = 5  # how long to show each bird animation

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0  # tilt of the bird
        self.tick_count = 0  # helper for defining the physics of the bird
        self.vel = 0  # speed of the bird
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5  # from the center of the screen
        self.tick_count = 0  # keeps track of when we last jumped
        self.height = self.y

    def move(self):
        self.tick_count += 1

        # bird physics (gravity)
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        # terminal velocity
        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d

        # tilt bird (animation)
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1  # keep track of how many times an image has been shown for (animation)

        # change the image to draw/show based on the img_count
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # don't animate wing flap when bird is going down
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # rotate bird around the center (tilt animation)
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


def draw_window(win, bird):
    win.blit(BG_IMG[0], (0, 0))
    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    # main loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(win, bird)

    pygame.quit()
    quit()


main()
