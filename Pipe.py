#
# Class representing pipe object
#
import random

import pygame as game


class Pipe:
    GAP = 200
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.image = game.image.load(r"Images/pipe-red.png").convert_alpha()
        self.image = game.transform.scale2x(self.image)
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = game.transform.flip(self.image, False, True)
        self.PIPE_BOTTOM = self.image
        self.passed = False
        self.set_height()

    def get_rectangles(self):
        return self.PIPE_TOP.get_rect(), self.PIPE_BOTTOM.get_rect()

    def set_height(self):
        self.height = random.randrange(50, 350)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VELOCITY


    def draw(self, screen):
        """
        A pipe is a both top and bottom pipe.

        :param screen: Screen object to draw image on
        """
        screen.blit(self.PIPE_TOP, (self.x, self.top))
        screen.blit(self.image, (self.x, self.bottom))

    def collied(self, bird):
        """
        Collision method basd on mask generated from the element's postion.
        Grant a score if the bird has pas the pipes + 30 pixels and its inbetween.

        :param bird: Bird object
        :return bool: Return true if collision occur else False
        """
        bird_mask = bird.get_mask()
        top_mask = game.mask.from_surface(self.PIPE_TOP)
        bottom_mask = game.mask.from_surface(self.image)
        # Calculate offset, it represents the distance of the bird to the pipe
        top_offset = (self.x - bird.x_position, self.top - round(bird.y_position))
        bottom_offset = (self.x - bird.x_position, self.bottom - round(bird.y_position))

        # finding point of collision/ overlap, if no overlap returns None
        top_point = bird_mask.overlap(top_mask, top_offset)
        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)

        if top_point or bottom_point:
            return True

        return False


#
# Class describing the base floor
#

class Base:
    VELOCITY = 5

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.image = game.image.load(r"Images/base.png").convert_alpha()
        self.image = game.transform.scale2x(self.image)
        self.width = self.image.get_width()
        self.x2 = self.width

    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        # check if the image has gotten out of screen, if so set it to the other's image position
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, screen):
        screen.blit(self.image, (self.x1, self.y))
        screen.blit(self.image, (self.x2, self.y))





