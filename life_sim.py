import pygame
import random
import time
import sys
sys.path.append('''C:/Users/james/Dropbox/Python/pygame/Asteroids/''')
import pygame_starter_pack as psp
import math

dt = .5
hunger_adder_per_sec = .4
max_speed = 30
max_sight = 300
class Bunny:

    def __init__(self, id_num, x, y, reprod_urge, male, hotness, speed, sight, hunger):

        self.age = 0
        self.hunger = hunger
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
        self.hop_cooldown = 5
        self.time_til_hop = 0
        self.hopping = False
        self.hop_time_remaining = 0
        self.hop_duration = 20
        self.speed = speed
        self.sight = sight
        self.top_priorities = ['reproduce', 'eat'] # 'eat','drink','reproduce'
        self.preggo = False
        self.preggo_time_period = 10
        self.preggo_time_left = 0
        self.gestational_period = 10
        self.gestation_time_left = 100
        self.mate = None

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
        self.x = min( max((self.x + self.vx * dt), 0), length)
        self.y = min( max((self.y + self.vy * dt), 0), width)
        self.hop_time_remaining = self.hop_time_remaining - dt

    def move(self, foods, bunnies):


        if self.time_til_hop <= 0 and not self.hopping:
            self.hopping = True
            self.hop_time_remaining = self.hop_duration

        if self.hopping:
            if self.hop_time_remaining == self.hop_duration:
                #just started the hop
                self.set_top_priority()
                self.get_hop_dir(foods, bunnies)

            if self.hop_time_remaining <= 0:
                self.hopping = False
                self.time_til_hop = self.hop_cooldown
                self.vx = 0
                self.vy = 0

            else:
                self.hop()

        else:
            self.time_til_hop -= dt

        self.hunger += hunger_adder_per_sec * dt
        if self.preggo:
            self.preggo_time_left -= dt

        if self.gestation_time_left > 0:
            self.gestation_time_left -= dt
        else:
            self.gestation_time_left = 0

    def seek(self, list, type):

        closest_dist = self.sight
        closest_ind = None

        for i in range(len(list)):
            dist = psp.get_dist(list[i].x, list[i].y, self.x, self.y)
            if dist < closest_dist:
                desirable = True
                if type == 'reproduce':
                    #see if the other is desirable
                    if (list[i].hotness * random.random()) < (self.reprod_urge):
                        desirable = False

                if desirable:
                    closest_dist = dist
                    closest_ind = i
        if closest_ind == None:
            return None

        #d = vt
        time = closest_dist / self.speed

        if time < self.hop_duration:
            self.hop_time_remaining = time

        angle_of_attack = psp.angle_from_1_to_2( self.x, self.y, list[closest_ind].x, list[closest_ind].y )
        return angle_of_attack

    def get_hop_dir(self, foods, bunnies):

        lists = []
        urges = []
        for i in self.top_priorities:

            if i == 'eat':
                lists.append(foods)
                urges.append(self.hunger)
            if i == 'reproduce':
                #get females
                list_to_check = []
                for bunny in bunnies:
                    if self.male:
                        if not bunny.male and not bunny.preggo:
                            list_to_check.append(bunny)
                    else:
                        if bunny.male:
                            list_to_check.append(bunny)
                lists.append(list_to_check)
                urges.append(self.reprod_urge)

        found = False
        try_to = True
        for i in range(len(lists)):
            if urges[i] != 0:

                if self.top_priorities[i] == 'reproduce':
                    if self.gestation_time_left > 0:
                        try_to = False


                if try_to:
                    angle_of_attack = self.seek(lists[i], self.top_priorities[i])
                    if angle_of_attack != None:
                        found = True
                        break

        if not found:
            angle_of_attack = random_angle()

        self.vx = self.speed * math.cos(angle_of_attack)
        self.vy = self.speed * math.sin(angle_of_attack)

    def set_top_priority(self):

        top_priorities = ['reproduce','eat']
        a = [self.reprod_urge, self.hunger]
        a, top_priorities = zip(*sorted(zip(a, top_priorities)))

        top = []
        for i in top_priorities:
            top.append(i)
        top.reverse()

        new = []
        for i in a:
            new.append(i)
        new.reverse()

        self.top_priorities = top

class Food:

    def __init__(self, x, y, color, radius):

        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.calories = 10

    def draw(self, screen):
        psp.draw_circle(screen, self.color, [self.x, self.y], self.radius)

class Water:

    def __init__(self, coords, color):

        self.coords = coords
        self.color = color

def genetics(mom_val, dad_val, maternal_fav, paternal_fav, variance, max_value, min_value):

    value = mom_val * maternal_fav + dad_val * paternal_fav
    value += (random.random() * variance * random.choice([-1,1]))
    value = max( min( max_value, value) ,   min_value)
    return value


def make_baby(mom, dad, id):

    #def __init__(self, id_num, x, y, reprod_urge, male, hotness, speed, sight):
    pat = random.random()
    reprod_urge = genetics(mom.reprod_urge, dad.reprod_urge, 1-pat, pat, 10, 100, 0)
    hotness = genetics(mom.hotness, dad.hotness, 1-pat, pat, 10, 100, 0)
    speed = genetics(mom.speed, dad.speed, 1-pat, pat, 3, max_speed, 1)
    sight = genetics(mom.sight, dad.sight, 1-pat, pat, 25, max_sight, 1)

    baby = Bunny(id, mom.x, mom.y, reprod_urge, random.choice([True, False]), hotness, speed, sight, (dad.hunger + mom.hunger) / 2)
    return baby


def check_newborn(bunnies, id):

    for bunny_num in range(len(bunnies)):
        bunny = bunnies[bunny_num]
        if bunny.preggo:
            if bunny.preggo_time_left <= 0:
                baby = make_baby(bunny, bunny.mate, id)
                bunnies[bunny_num].preggo = False
                bunnies.append(baby)
                id += 1
    return bunnies, id

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

def check_eaten(bunnies, foods):

    eaten = []
    for bunny in bunnies:
        if bunny.hunger > 0:
            for food_num in range(len(foods)):
                if psp.detect_collision(bunny.x, bunny.y, foods[food_num].x, foods[food_num].y, bunny.radius):
                    eaten.append(food_num)
                    bunny.hunger -= foods[food_num].calories
                    if bunny.hunger < 0:
                        bunny.hunger = 0

    foods = delete_these_inds(foods, eaten)
    return foods

def check_dead_bunnies(bunnies):

    dead = []
    for bunny_num in range(len(bunnies)):
        if bunnies[bunny_num].hunger > 100:
            dead.append(bunny_num)

    bunnies = delete_these_inds(bunnies, dead)
    return bunnies

def check_reproduction(bunnies):

    for bunny_num in range(len(bunnies)):
        for bunny_num2 in range(len(bunnies)):
            b1 = bunnies[bunny_num]
            b2 = bunnies[bunny_num2]

            collide = psp.detect_collision(b1.x, b1.y, b2.x,b2.y, b1.radius)
            if collide:
                if b1.gestation_time_left <= 0 and b2.gestation_time_left <= 0:
                    if b1.male != b2.male:
                        #different genders
                        if (not b1.preggo) and (not b2.preggo):
                            #neither is pregnant already
                            #see if the male is desirable
                            if not b1.male:
                                ind = bunny_num
                                mate_ind = bunny_num2
                            if not b2.male:
                                ind = bunny_num2
                                mate_ind = bunny_num

                            test_num = random.random() * 100
                            if bunnies[mate_ind].hotness > test_num:

                                bunnies[ind].preggo = True
                                bunnies[ind].preggo_time_left = bunnies[ind].preggo_time_period
                                bunnies[ind].mate = bunnies[mate_ind]

    return bunnies

length = 1000
width = 700
screen = psp.get_screen(length, width)
clock = pygame.time.Clock()

background_color = (0,0,0)

max_food = 35
food_color = (102, 255, 102)
food_radius = 4

dad = Bunny(1, 250, 250, 50, True, 50, 3, 150, 0)
mom = Bunny(2, 250, 250, 50, True, 50, 3, 150, 0)

bunnies = []
for i in range(100):
    new = make_baby(mom, dad, i + 3)
    new.x = random.random() * length
    new.y = random.random() * width
    bunnies.append(new)



foods = []
for i in range(max_food):
    x,y = random_xys_in_bounds(length, width)
    foods.append( Food(x,y, food_color, food_radius) )

running = True
id = 23
cur_bunnies = len(bunnies)

bunnies_num = []
hotness_avg = []
speed_avg = []
reprod_urge_avg = []
sight_avg = []
last_time = time.time()
while running:

    screen.fill(background_color)

    if len(foods) < max_food:
        x,y = random_xys_in_bounds(length, width)
        foods.append( Food(x,y, food_color, food_radius) )
    for i in bunnies:
        i.move(foods, bunnies)
        i.draw(screen)
    for i in foods:
        i.draw(screen)

    foods = check_eaten(bunnies, foods)
    bunnies = check_dead_bunnies(bunnies)
    bunnies = check_reproduction(bunnies)
    bunnies, id = check_newborn(bunnies, id)

    if len(bunnies) != cur_bunnies:
        cur_bunnies = len(bunnies)
        print (cur_bunnies)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    psp.flip_screen()
    clock.tick(120)

    if int(time.time()) > last_time:
        last_time = int(time.time())
        bunnies_num.append(len(bunnies))

        hotness = []
        for i in bunnies:
            hotness.append(i.hotness)
        hotness_avg.append( sum(hotness) / len(hotness) )

        reprod_urge = []
        for i in bunnies:
            reprod_urge.append(i.reprod_urge)
        reprod_urge_avg.append( sum(reprod_urge) / len(reprod_urge) )

        speed = []
        for i in bunnies:
            speed.append(i.speed)
        speed_avg.append(sum(speed) / len(speed))

        sight = []
        for i in bunnies:
            sight.append(i.sight)
        sight_avg.append( sum(sight) / len(sight))

    if len(bunnies) == 0 or len(bunnies) > 200:
        running = False


    if pygame.key.get_focused():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            running = False
            pygame.quit()

import matplotlib.pyplot as plt

print (bunnies_num)
print (hotness_avg)

a = plt.scatter(list(range(len(bunnies_num))), bunnies_num)
b = plt.scatter(list(range(len(hotness_avg))), hotness_avg)
c = plt.scatter(list(range(len(reprod_urge_avg))),reprod_urge_avg)
d= plt.scatter(list(range(len(speed_avg))), speed_avg)
e= plt.scatter(list(range(len(sight_avg))) , sight_avg)
plt.legend((a,b,c,d,e), ('Bunnies','Hotness','Reproductive Urge','Speed','Sight'))
plt.show()
