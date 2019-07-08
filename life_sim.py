import pygame
import random
import time
import sys
sys.path.append('''C:/Users/UVYGBK4/Documents/python/Asteroids/''')
import pygame_starter_pack as psp
import math

dt = 1

class Bunny:

    def __init__(self, id_num, x, y, reprod_urge, male, hotness, speed, sight):

        self.age = 0
        self.hunger = 0
        self.thirst = 0
        self.radius = 5

        self.id_num = id_num
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.reprod_urge = reprod_urge #0 and 100
        self.hotness = hotness #between 0 and 100
        self.male = male

        self.color = self.get_bunny_color()
        self.hop_cooldown = 30
        self.time_til_hop = 0
        self.hopping = False
        self.hop_time_remaining = 0
        self.hop_duration = 10
        self.speed = speed
        self.sight = sight


    def draw(self, screen):

        psp.draw_circle(screen, self.color, [self.x, self.y], self.radius)

    def get_bunny_color(self):

        ugly_male = (171,212,255)
        hot_male = (0,123, 255)
        ugly_female = (255, 171,249)
        hot_female = (255, 0, 238)

        if self.male:
            hot = hot_male
            ugly = ugly_male
        else:
            hot = hot_female
            ugly = ugly_female

        a = self.hotness

        prop = a / 100
        rdif = hot[0] - ugly[0]
        gdif = hot[1] - ugly[1]
        bdif = hot[2] - ugly[2]

        r = int(prop * (rdif) + ugly[0])
        g = int(prop * (gdif) + ugly[1])
        b = int(prop * (bdif) + ugly[2])
        return (r,g,b)

    def hop(self):
        self.x = (self.x + self.vx * dt)
        self.y = (self.y + self.vy * dt)
        self.hop_time_remaining = self.hop_time_remaining - dt

    def move(self):

        if self.time_til_hop <= 0 and not self.hopping:
            self.hopping = True
            self.hop_time_remaining = self.hop_duration

        if self.hopping:
            if self.hop_time_remaining == self.hop_duration:
                #just started the hop
                self.get_hop_dir()

            if self.hop_time_remaining <= 0:
                self.hopping = False
                self.time_til_hop = self.hop_cooldown
                self.vx = 0
                self.vy = 0

            else:
                self.hop()

        else:
            self.time_til_hop -= dt


    def get_hop_dir(self):
        angle = random_angle()
        self.vx = self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)

class Food:

    def __init__(self, x, y, color, radius):

        self.x = x
        self.y = y
        self.color = color
        self.radius = radius

    def draw(self, screen):
        psp.draw_circle(screen, self.color, [self.x, self.y], self.radius)

class Water:

    def __init__(self, coords, color):

        self.coords = coords
        self.color = color


def random_xys_in_bounds(xupper, yupper):

    x =int ( random.random() * xupper )
    y =int ( random.random() * yupper )
    return x,y

def delete_these_inds(list, inds):

    for i in range(len(list) -1, -1, -1):
        if i in inds:
            del list[i]
    return list

def random_angle():
    return random.random() * math.pi * 2



background_color = (0,0,0)

max_food = 50
food_color = (102, 255, 102)
food_radius = 4

bunnies = [Bunny(1, 250, 250, 100, True, 0, 5, 100), Bunny(1, 500, 500, 100, False, 0, 3, 100)]
foods = []
print (bunnies[0].color)

length = 1000
width = 700

screen = psp.get_screen(length, width)
clock = pygame.time.Clock()

running = True
while running:

    screen.fill(background_color)

    if len(foods) < max_food:
        x,y = random_xys_in_bounds(length, width)
        foods.append( Food(x,y, food_color, food_radius) )

    for i in bunnies:
        i.move()
        i.draw(screen)
    for i in foods:
        i.draw(screen)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    psp.flip_screen()
    clock.tick(120)
