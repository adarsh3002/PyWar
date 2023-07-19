import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random

# globals for user interface
# only finite number of missiles!
WIDTH = 800
HEIGHT = 600
ROCKLIMITSET = 5
AMMOLIMIT = 4
EXTRALIFELIMIT = 1
MISSILE_LIFE = 75
score = 0
lives = 3
time = 0
INV_TIME = 120
god_time = INV_TIME
started = False
missile_inventory = 10
PI = 3.141592654
FRICTION = 0.99
MISSILE_ANGLE_FRICTION = 0.95
ROTATION_SPEED = 0.1
# only able to lock within viewing range (ie, PI / 3 = 60 degrees)
LOCK_ANGLE_RANGE = PI / 6
# speed in which angle changes to lock target
LOCK_ANGLE_VEL_SPEED = 2 * PI / 36
# if angle between lock target and object is within tolerance, leave it
LOCK_ANGLE_TOLERANCE = 2 * PI / 12
ROCKLIMIT = ROCKLIMITSET
level = 1

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated
        

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris1_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
#n1 = simplegui.load_image("https://www.dropbox.com/s/r0rmfxpbh0lshyx/heic0619a_800x600.png?dl=1")
#n2 = simplegui.load_image("https://www.dropbox.com/s/93jayn2ot84io2o/eso1137_hubble_dark_800x600.png?dl=1")
#n1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")
#n2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_brown.png")
n3 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")
n4 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_brown.png")
n1 = simplegui.load_image("https://www.dropbox.com/s/r0rmfxpbh0lshyx/heic0619a_800x600.png?dl=1")
n2 = simplegui.load_image("https://www.dropbox.com/s/93jayn2ot84io2o/eso1137_hubble_dark_800x600.png?dl=1")

nebulas =[n3, n4]
nebula_image = random.choice(nebulas)

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")
# https://www.dropbox.com/s/0a6ymdeyiypzgxa/small_splash.png=?dl=1
#splash_info = ImageInfo([150, 26], [300, 55])
#splash_image = simplegui.load_image("https://www.dropbox.com/s/0a6ymdeyiypzgxa/small_splash.png?dl=1")


# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, MISSILE_LIFE)
ammo_info = ImageInfo([5, 5], [10, 10], 20)
missile_image1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")
missile_image2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
missile_image3 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot3.png")
missile_images=list()
#missile_images.append(missile_image1)
#missile_images.append(missile_image2)
missile_images.append(missile_image3)


# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
asteroid_image2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png")
asteroid_image3 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")
asteroid_imageb = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")

asteroid_imageb = simplegui.load_image("http://otoro.net/misc/astroids/brok.jpg")
asteroid_images=list()
asteroid_images.append(asteroid_image1)
asteroid_images.append(asteroid_image2)
asteroid_images.append(asteroid_image3)
#asteroid_images.append(asteroid_imageb)

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_dim = [9, 9] # i used the more awesome physics generated explosion template
explosion_life = 74 # only first 74 pics look good.
#explosion_info = ImageInfo([64, 64], [128, 128], 17, explosion_life, True)
explosion_info = ImageInfo([50, 50], [100, 100], 17, explosion_life, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/explosion.hasgraphics.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist2(p, q):
    return (p[0] - q[0]) * (p[0] - q[0]) + (p[1] - q[1]) * (p[1] - q[1])

def dist(p, q):
    return math.sqrt(dist2(p, q))

def get_angle(p, q):
    return math.atan2(q[1]-p[1],q[0]-p[0])

def get_angle_diff(p, q):
    angle_diff = (p-q)%(2*PI)
    angle_diff2 = 2*PI - angle_diff
    if angle_diff < angle_diff2:
        return angle_diff
    return -angle_diff2

# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.locktarget = None
        
    def draw(self,canvas):
        global god_time
        drawship = True
        if god_time > 0: #  and god_time % 2 == 0
            canvas.draw_circle(self.pos, self.radius, 1, "Yellow")
        if self.thrust and drawship:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        elif drawship:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if self.locktarget != None:
            global rock_group, mini_rock_group
            lockrock = self.locktarget
            if (lockrock in rock_group) or (lockrock in mini_rock_group):
                canvas.draw_circle(lockrock.pos, lockrock.radius*lockrock.scale, 3, "lime")
            else:
                lockrock = None
    


    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .2
            self.vel[1] += acc[1] * .2
            
        self.vel[0] *= FRICTION
        self.vel[1] *= FRICTION

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += ROTATION_SPEED
        
    def decrement_angle_vel(self):
        self.angle_vel -= ROTATION_SPEED
        
    def shoot(self):
        global missile_group, missile_inventory, score, rock_group, mini_rock_group
        if missile_inventory > 0:
            missile_inventory -= 1
            #vel = 4 + score / 5
            #vel = min(24, vel)
            vel = 0
            avel = self.angle_vel
            forward = angle_to_vector(self.angle)
            missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
            missile_vel = [self.vel[0] + vel * forward[0], self.vel[1] + vel * forward[1]]
            a_missile = Sprite(missile_pos, missile_vel, self.angle, avel, random.choice(missile_images), missile_info, missile_sound)
            a_missile.lifespan += min(score, 3*MISSILE_LIFE)
            a_missile.accel = 0.2
            a_missile.avel_friction = MISSILE_ANGLE_FRICTION
            a_missile.scale = 1.5
            if self.locktarget != None:
                a_missile.locktarget = self.locktarget
                # as a twist, assign a random rock to lock onto ship!
                allrock = set(rock_group.union(mini_rock_group))
                allrock.difference_update(set([self.locktarget]))
                prey = None
                if len(allrock) > 0:
                    prey = random.choice(list(allrock))
                if prey != None:
                    target_angle = get_angle(prey.pos,self.pos)
                    prey.angle = target_angle
                    prey.locktarget = self
                    prey.avel = 0.0
                    prey.accel = 0.05
            missile_group.add(a_missile)
            self.locktarget = None
    
    def setlock(self):
        global rock_group, mini_rock_group
        allrock = set(rock_group.union(mini_rock_group))
        allrock_copy = set(allrock)
        ship_angle = self.angle
        for rock in allrock_copy:
            target_angle = get_angle(self.pos,rock.pos)
            
            angle_diff = get_angle_diff(ship_angle, target_angle)
            
            if abs(angle_diff) > LOCK_ANGLE_RANGE:
                allrock.remove(rock)
        allrock = list(allrock)
        if len(allrock) > 0:
            d = float('inf')
            for rock in allrock:
                d2 = dist2(rock.pos, self.pos)
                if d2 < d:
                    d = d2
                    target_candidate = rock
            #target_candidate = random.choice(allrock) 
            if self.locktarget == target_candidate:
                self.locktarget = None
            else:
                self.locktarget = target_candidate
                #target_angle = get_angle(self.pos, target_candidate.pos)
                #angle_diff = get_angle_diff(ship_angle, target_angle)
                #print "angle between target and ship", 360*angle_diff/(2*PI)
                
        else:
            self.locktarget = None
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.scale = 1.0
        self.age = 0
        self.accel = 0.0
        self.avel_friction = 1.0
        self.locktarget = None
        if sound:
            sound.rewind()
            sound.play()
            
    def set_scale(self, scale):
        self.scale = scale
   
    def draw(self, canvas):
        index = [0, 0]
        if self.animated:
            index = [self.age % explosion_dim[0], (self.age // explosion_dim[0]) % explosion_dim[1]]
        new_center = [0, 0]
        new_center[0] = self.image_center[0] + index[0]*self.image_size[0]
        new_center[1] = self.image_center[1] + index[1]*self.image_size[1]
        draw_size = [0, 0]
        draw_size[0] = self.image_size[0]*self.scale
        draw_size[1] = self.image_size[1]*self.scale
        canvas.draw_image(self.image, new_center, self.image_size,
                          self.pos, draw_size, self.angle)
        if self.locktarget != None:
            global rock_group, mini_rock_group
            lockrock = self.locktarget
            if not (lockrock in rock_group) and not (lockrock in mini_rock_group):
            #    canvas.draw_circle(lockrock.pos, lockrock.radius*lockrock.scale, 1, "green")
            #else:
                lockrock = None
        
    def update(self):
        global my_ship
        aged = False
        
        # if target has lock, change angle vel by a bit.
        if self.locktarget != None :
            d = dist(self.pos, my_ship.pos)

            if (d > 1.5 * my_ship.radius):
                target_angle = get_angle(self.pos, self.locktarget.pos)
                angle_diff = get_angle_diff(self.angle, target_angle)
                if abs(angle_diff) > LOCK_ANGLE_TOLERANCE:
                    self.angle_vel = 0
                    if angle_diff > 0:
                        self.angle -= LOCK_ANGLE_VEL_SPEED
                    else:
                        self.angle += LOCK_ANGLE_VEL_SPEED
                else:
                    
                    if angle_diff > 0:
                        self.angle_vel -= LOCK_ANGLE_VEL_SPEED
                    else:
                        self.angle_vel += LOCK_ANGLE_VEL_SPEED                    
            #LOCK_ANGLE_VEL_SPEED
            #LOCK_ANGLE_TOLERANCE

        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        if self.accel > 0:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * self.accel
            self.vel[1] += acc[1] * self.accel
            self.vel[0] *= FRICTION
            self.vel[1] *= FRICTION
            self.angle_vel *= self.avel_friction

        self.age += 1
        if self.age > self.lifespan:
            aged = True
        return aged
    
    def collide(self, other): # implementation is faster than using sqrt.
        collision = False
        r = self.radius*self.scale + other.radius
        dx = self.pos[0]-other.pos[0]
        dy = self.pos[1]-other.pos[1]
        d2 = dx*dx + dy*dy
        r2 = r*r
        if d2 < r2:
            collision = True
        return collision
  
        
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
    elif key == simplegui.KEY_MAP['z']:
        my_ship.setlock()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score, missile_inventory, nebulas, nebula_image, level
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        nebula_image = random.choice(nebulas)
        started = True
        lives = 3
        if level == 1:
            score = 0
        missile_inventory = 10
        rock_spawner2()
        

def process_sprite_group(group, canvas):
    copygroup = set(group)
    for item in copygroup:
        item.draw(canvas)
        aged = item.update()
        if aged:
            group.remove(item)

def create_children(item):
    global mini_rock_group
    if item.scale >= 1.0 and item.locktarget == None:
        rock1_pos = item.pos
        rock1_vel = item.vel
        rock1_angle = item.angle
        rock1_avel = item.angle_vel
        rock1 = Sprite(rock1_pos, rock1_vel, rock1_angle, rock1_avel, item.image, asteroid_info)
        rock2_pos = item.pos
        rock2_vel = [0, 0]
        rock2_vel[0] = rock1_vel[0] * -1
        rock2_vel[1] = rock1_vel[1] * -1
        rock2_angle = rock1_angle * -1
        rock2_avel = rock1_avel * -1
        rock2 = Sprite(rock2_pos, rock2_vel, rock2_angle, rock2_avel, item.image, asteroid_info)
        rock1.scale = 0.5
        rock2.scale = 0.5
        rock1.accel = item.accel
        rock2.accel = item.accel
        mini_rock_group.add(rock1)
        mini_rock_group.add(rock2)
            
def group_collide(group, other):
    global explosion_group, explosion_sound
    copygroup = set(group)
    collision = False
    for item in copygroup:
        if item.collide(other):
            collision = True
            # create new explosion
            explosion = Sprite(item.pos, item.vel, item.angle, item.angle_vel, explosion_image, explosion_info)
            explosion.scale = item.scale*0.8
            explosion_group.add(explosion)
            explosion_sound.rewind()
            explosion_sound.play()
            create_children(item)
            group.remove(item)
    return collision

def group_group_collide(group, other_group):
    global score
    copygroup = set(group)
    for item in copygroup:
        if group_collide(other_group, item):
            group.remove(item)
            score += 1
    
        
def draw(canvas):
    global level, time, life_group, god_time, nebula_image, nebulas, started, ammo_group, mini_rock_group, rock_group, missile_group, my_ship, score, lives, asteroid_images, ROCKLIMIT, missile_inventory
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    #update rocks
    process_sprite_group(rock_group, canvas)
    process_sprite_group(mini_rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    process_sprite_group(ammo_group, canvas)
    process_sprite_group(life_group, canvas)
    
    for item in life_group:
        canvas.draw_circle(item.pos, item.radius*item.scale, 1, "Blue")
        if item.collide(my_ship):
            life_group.remove(item)
            lives +=1
            god_time = INV_TIME*2

    for item in ammo_group:
        canvas.draw_circle(item.pos, item.radius, 1, "Red")
        if item.collide(my_ship):
            ammo_group.remove(item)
            missile_inventory += 10
    #canvas.draw_circle(my_ship.pos, my_ship.radius, 1, "Red")
    
    # draw ship and sprites
    my_ship.draw(canvas)
    
    # update ship and sprites
    my_ship.update()

    
    # check collision between ship and rocks
    if god_time == 0:
        if group_collide(rock_group, my_ship):
            lives-=1
            god_time = INV_TIME
        if group_collide(mini_rock_group, my_ship):
            lives-=1
            god_time = INV_TIME
    
    if lives < 0:
        lives = 0
    
    # check collision between rocks and missiles
    group_group_collide(missile_group, rock_group)
    group_group_collide(missile_group, mini_rock_group)
    
    # check for death
    if lives <= 0:
        level = 1
        missile_group = set()
        rock_group = set()
        ammo_group = set()
        mini_rock_group = set()
        life_group = set()
        started = False
        soundtrack.rewind()
        soundtrack.play()
        ROCKLIMIT = ROCKLIMITSET

    # check if win
    if (len(mini_rock_group) + len(rock_group) == 0) and started:
        level += 1
        # add secret image if level >= 2
        if level > 1 and len(asteroid_images) < 4:
            asteroid_images.append(asteroid_imageb)
        if level > 2:
            nebulas.append(n1)
            nebulas.append(n2)
        ROCKLIMIT += 1

        missile_group = set()
        rock_group = set()
        ammo_group = set()
        mini_rock_group = set()
        life_group = set()
        started = False
        soundtrack.rewind()
        soundtrack.play()
        ROCKLIMIT = ROCKLIMITSET
    #

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        if level == 1:
            canvas.draw_text("Hit Spacebar to shoot, Hit Z to lock on a target", [50, 500], 24, "White", "monospace")
        else:
            canvas.draw_text("Starting Level "+str(level)+" soon.", [50, 500], 32, "White", "monospace")
            
    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "Lime", "monospace")
    canvas.draw_text("Missile", [200, 50], 22, "Red", "monospace")
    canvas.draw_text("Level", [350, 50], 22, "Yellow", "monospace")
    canvas.draw_text("Score", [680, 50], 22, "White", "monospace")
    canvas.draw_text(str(lives), [50, 80], 22, "White", "monospace")
    canvas.draw_text(str(score), [680, 80], 22, "White", "serif")
    canvas.draw_text(str(missile_inventory), [200, 80], 22, "White", "monospace")
    canvas.draw_text(str(level), [350, 80], 22, "White", "monospace")
    
    god_time -= 1
    if god_time < 0:
        god_time = 0
        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, my_ship, score, started, mini_rock_group, level
    if len(rock_group) + len(mini_rock_group) >= ROCKLIMIT:
        return
    speed = math.sqrt(max(level*30,1)) # increase speed as score increases
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    rock_vel = [(random.random() * .6 - .3)*speed*1, (random.random() * .6 - .3)*speed*1]
    rock_avel = (random.random() * .08-0.04)
    a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, random.choice(asteroid_images), asteroid_info)
#    a_rock.accel = (random.random() * 0.2 - 0.1)*speed
    #a_rock.avel_friction = 0.999
    if (dist(my_ship.pos, a_rock.pos) > my_ship.radius*5 and started):  # make sure rocks are within 5 ships distance
        rock_group.add(a_rock)

def rock_spawner2():
    global rock_group, my_ship, score, started, mini_rock_group, level, ROCKLIMIT
    while len(rock_group) + len(mini_rock_group) <= ROCKLIMIT:
        speed = math.sqrt(max(level*30,1)) # increase speed as score increases
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [(random.random() * .6 - .3)*speed*1, (random.random() * .6 - .3)*speed*1]
        rock_avel = (random.random() * .08-0.04)
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, random.choice(asteroid_images), asteroid_info)
        if (dist(my_ship.pos, a_rock.pos) > my_ship.radius*8 and started):  # make sure rocks are within 8 ships distance
            rock_group.add(a_rock)

# timer handler that spawns a ammo unit    
def ammo_spawner():
    global ammo_group, my_ship, started
    if len(ammo_group) >= AMMOLIMIT:
        return
    ammo_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    ammo_vel = [(random.random() * .6 - .3), (random.random() * .6 - .3)]
    ammo_avel = random.random() * .2 - .1
    ammo = Sprite(ammo_pos, ammo_vel, 0, ammo_avel, missile_image3, ammo_info)
    if (dist(my_ship.pos, ammo.pos) > my_ship.radius*3 and started):  # make sure ammo are within 3 ships distance
        ammo_group.add(ammo)
            
# timer handler that spawns an extra life unit    
def life_spawner():
    global life_group, my_ship, started
    if len(life_group) >= EXTRALIFELIMIT:
        return
    pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    vel = [(random.random() * .6 - .3), (random.random() * .6 - .3)]
    life = Sprite(pos, vel, 3*PI/2, 0, ship_image, ship_info)
    life.scale = 0.5
    if (dist(my_ship.pos, life.pos) > my_ship.radius*6 and started):  # make sure ammo are within 3 ships distance
        life_group.add(life)

# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, .1, asteroid_image, asteroid_info)
rock_group = set()
mini_rock_group = set()
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
missile_group = set()
ammo_group = set()
life_group = set()
explosion_group = set()

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

#timer = simplegui.create_timer(1000.0, rock_spawner)
timer2 = simplegui.create_timer(3333.3, ammo_spawner)
timer3 = simplegui.create_timer(8888.8, life_spawner)

# get things rolling
#timer.start()
timer2.start()
timer3.start()
frame.start()

soundtrack.rewind()
soundtrack.play()
