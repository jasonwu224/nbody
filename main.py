import pygame, json, random as rand
from uuid import uuid4
from system import System
from ball import Ball

######INIT######

pygame.init()

#####METHODS#####

def create_system(n: int, size: tuple[int, int]) -> System:
    balls = []
    width, height = size
    for i in range(n):
        rand_mass = (1 + rand.random()) * 10**12
        rand_x = rand.randint(100, width-100)
        rand_y = rand.randint(100, height-100)
        balls.append(Ball(rand_mass, (rand_x, rand_y)))

    return System(balls)

def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#####CONSTANTS#####
# unsure what this unit is, probably meters
width, height = 1000, 700
SIZE = width, height
BLACK = 0, 0, 0
WHITE = 255, 255, 255
FONT_SIZE = 20
TEXT_FONT = pygame.font.SysFont("Arial", FONT_SIZE)
# timestep = 5  # ms
# if ratio is 2, 2x speed compared to timestep
SPEED_OF_TIME_RATIO = 10
FRAMERATE = 50
NUM_BALLS = 10

####OBJECTS#####

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
system = create_system(NUM_BALLS, SIZE)

init_system_list = system.to_list()
####LOOP#####

running = True
dt = 0
time_elapsed = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False

    for i in range(SPEED_OF_TIME_RATIO):
        system.update(dt)

    tot_p, tot_E = system.get_info()
    # tiny momentum and energy are rounded to 0
    tot_p = round(tot_p, 0)  
    tot_E = round(tot_E, 0)

    screen.fill(BLACK)

    for ball in system.balls:
        pygame.draw.circle(screen, WHITE, ball.r, ball.get_radius())
    # format info
    momentum_string = "momentum: {:.2e}".format(tot_p)
    energy_string = "energy: {:.2e}".format(tot_E)
    sim_time_elapsed = int(SPEED_OF_TIME_RATIO*(time_elapsed / 1000))
    time_string = "time elapsed: {}".format(sim_time_elapsed)
    # draw info
    draw_text(screen, momentum_string, TEXT_FONT, WHITE, 10, 10)
    draw_text(screen, energy_string, TEXT_FONT, WHITE, 10, 10 + FONT_SIZE)
    draw_text(screen, time_string, TEXT_FONT, WHITE, 10, 10 + 2*FONT_SIZE)

    pygame.display.flip()

    # pygame.time.delay(framestep)
    dt = clock.tick(FRAMERATE)
    time_elapsed += dt

# save to file
if True:
    rand_id = str(uuid4())
    data = {
        "id": rand_id,
        "framerate" : FRAMERATE,
        "time_elapsed": time_elapsed,
        "init_num_balls": NUM_BALLS,
        "final_num_balls": len(system.balls),
        "units": {"mass": "kg", 
                  "dens": "kg/m^3", 
                  "pos": "m", 
                  "vel": "m/s", 
                  "time": "s"},
        "system": init_system_list
    }
    with open("saves.txt", "a") as file:
        json.dump(data, file)
        file.write("\n")

###QUIT####

pygame.quit()

'''
TODO:
save the info of each orbit to a file so it can
be resimulated
data should include: number of balls, framerate, configuration of each ball

add collisionless option (with softening gravitational force at small r)
add particle cloud version
add random inital velocity

make units accurate to real planets

preset config for stable 3 body orbits

add user configuration
button to create new random config
text box for number of balls
place balls and configure it

add widgets 
a slider for speed or button to show/hide info

compute total angular velocity?

create galaxy density distribution 
'''