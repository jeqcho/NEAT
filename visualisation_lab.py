import sys
import pygame
import random
import math
import copy
import math
pygame.init()

animate_flag = True
speed_val = 3

screen_size = screen_width, screen_height = 500, 500

screen = pygame.display.set_mode(screen_size)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))

eyesight_surface = pygame.Surface(screen_size)
eyesight_surface.fill((255, 255, 255))
eyesight_surface.set_alpha(40)


def reset():
    global bots, foods, eyesights, all_sprites
    bots = pygame.sprite.Group()
    foods = pygame.sprite.Group()
    eyesights = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()


reset()


class EyeSight(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.range = 50
        self.diameter = 2 * self.range
        self.sense = {}
        self.x = x
        self.y = y
        self.image = pygame.Surface((self.diameter, self.diameter))
        # self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.left = x - self.range
        self.rect.top = y - self.range
        self.add(eyesights)
        # self.add(all_sprites)

    def show(self):
        pygame.draw.circle(eyesight_surface, (255, 0, 0), (self.x, self.y), self.range, 0)

    def grow(self, new_height, bot_height):
        self.range = int(self.range * new_height / bot_height)
        self.diameter = 2 * self.range
        self.image = pygame.transform.scale(self.image, [self.diameter, self.diameter])
        self.rect.width = self.diameter
        self.rect.height = self.diameter

    def move_(self, new_pos, bot_width, bot_height):
        # for centre of eyesight
        eyesight_new_pos = new_pos.copy()
        eyesight_new_pos.left += int(bot_width / 2)
        eyesight_new_pos.top += int(bot_height / 2)
        self.x = eyesight_new_pos.left
        self.y = eyesight_new_pos.top
        # for eyesight rect
        eyesight_new_pos.left -= self.range
        eyesight_new_pos.top -= self.range
        eyesight_new_pos.width = self.diameter
        eyesight_new_pos.height = self.diameter
        self.rect = eyesight_new_pos


class Bot(pygame.sprite.Sprite):
    def __init__(self, color, x, y, speed=(0, 0)):
        pygame.sprite.Sprite.__init__(self)

        self.species_size = self.species_width, self.species_height = 20, 20
        self.size = self.width, self.height = self.species_width, self.species_height
        self.color = color
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.area = screen.get_rect()
        self.rect.left = x - self.width / 2
        self.rect.top = y - self.height / 2
        self.speed = [speed[0], speed[1]]
        self.health_bar = 100
        self.add(bots)
        self.add(all_sprites)
        self.eyesight = EyeSight(x, y)

    def eat(self, energy_value):
        self.health_bar += energy_value

    def update(self, response):
        self.action(response)
        blocked = self.move_()
        self.grow()
        # self.metabolise()
        return self.speed + [blocked]

    def action(self,response):
        self.speed = [0, 0]
        if response[0] > response[1]:
            self.speed[0] = -speed_val
        elif response[0] < response[1]:
            self.speed[0] = speed_val
        if response[2] > response[3]:
            self.speed[1] = speed_val
        elif response[2] < response[3]:
            self.speed[1] = -speed_val

    def move_(self):
        blocked = 0
        new_pos = self.rect.move(self.speed)
        if not self.area.contains(new_pos):
            blocked = 1
            if self.rect.left <= self.area.left:
                new_pos[0] = 0
            if self.rect.right >= self.area.right:
                new_pos[0] = screen_width - self.width
            if self.rect.top <= self.area.top:
                new_pos[1] = 0
            if self.rect.bottom >= self.area.bottom:
                new_pos[1] = screen_height - self.height
        self.rect = new_pos
        self.eyesight.move_(new_pos, self.width, self.height)
        return blocked

    def grow(self):
        new_height = int(self.species_height * math.sqrt(self.health_bar / 100))
        new_width = int(self.species_width * math.sqrt(self.health_bar / 100))
        new_size = new_width, new_height
        if not (self.size == new_size):
            self.image = pygame.transform.scale(self.image, new_size)
            self.eyesight.grow(new_height, self.height)
            self.size = self.width, self.height = new_size
            self.rect.width = new_width
            self.rect.height = new_height


food_width = 5
food_height = 5


class Food(pygame.sprite.Sprite):
    def __init__(self, food_id, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.id = food_id
        self.image = pygame.Surface([food_width, food_height])
        self.image.fill((0, 200, 0))
        self.x = x
        self.y = y

        self.rect = self.image.get_rect()
        self.area = screen.get_rect()
        self.rect.top = self.y - food_height / 2
        self.rect.left = self.x - food_width / 2

        self.energy_value = 6
        self.add(foods)
        self.add(all_sprites)


def compete(bot1_, bot2_):
    if bot1_.health_bar > bot2_.health_bar:
        bot1_.health_bar += bot2_.health_bar
        bot2_.health_bar = 0
        bot2_.kill()
    elif bot1_.health_bar < bot2_.health_bar:
        bot2_.health_bar += bot1_.health_bar
        bot1_.health_bar = 0
        bot1_.kill()
