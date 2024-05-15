import pygame, json, random as rand
from uuid import uuid4
from system import System
from ball import Ball

######INIT######

pygame.init()
#####METHODS#####

def load_system(id: str, path: str) -> System:
    # note that this should load framerate too, but I always keep it at 50
    with open(path, "r") as file:
        json_str = file.readline()

        while json_str != "":
            data = json.loads(json_str)
            # if found
            if data["id"] == id:
                ball_list = [Ball(**dict) for dict in data["system"]]
                return System(ball_list)
            
            json_str = file.readline()
    # if not found, raise error
    raise FileNotFoundError()

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
NUM_BALLS = 50
# ratio pixel:meters
DIST_SCALE = 1

####OBJECTS#####

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

sys_type = "e"
if sys_type == "random":
    system = create_system(NUM_BALLS, SIZE)
elif sys_type == "load":
    system = load_system("103c21ed-b63a-459b-bf19-d39e9367a91b", "saves.txt")
else:
    # earth moon
    DIST_SCALE = 1e-7
    TIME_SCALE = 1e6

    m_E = 5.972e24
    m_m = 7.34767309e22

    r_E = (width/4, height/2)
    dist = 384.4e6
    r_m = (width/4 + DIST_SCALE*dist, height/2)
    
    v_m = (0, 1022)

    d_E = .5514  # density
    d_m = .3344
    earth = Ball(m_E, r_E, d=d_E, dist_scale=DIST_SCALE)
    moon = Ball(m_m, r_m, v_m, d=d_m, dist_scale=DIST_SCALE)
    system = System([earth, moon], DIST_SCALE, TIME_SCALE)

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

    tot_p, tot_L, tot_E = system.get_info()
    # tiny momentum and energy are rounded to 0
    tot_p = round(tot_p, 0)  
    tot_E = round(tot_E, 0)
    tot_L = round(tot_L, 0)

    screen.fill(BLACK)

    for ball in system.balls:
        print(DIST_SCALE * ball.r, DIST_SCALE * ball.get_radius())
        pygame.draw.circle(screen, 
                           WHITE, 
                           DIST_SCALE * ball.r, 
                           DIST_SCALE * ball.get_radius())
    pygame.draw.circle(screen, WHITE, system.get_center_of_mass(), 1)
    # format info
    momentum_str = "momentum: {:.2e}".format(tot_p)
    ang_momentum_str = "ang momentum: {:.2e}".format(tot_L)
    energy_str = "energy: {:.2e}".format(tot_E)
    sim_time_elapsed = int(SPEED_OF_TIME_RATIO*(time_elapsed / 1000))
    time_str = "time elapsed: {}".format(sim_time_elapsed)
    # draw info
    draw_text(screen, momentum_str, TEXT_FONT, WHITE, 10, 10)
    draw_text(screen, ang_momentum_str, TEXT_FONT, WHITE, 10, 10 + FONT_SIZE)
    draw_text(screen, energy_str, TEXT_FONT, WHITE, 10, 10 + 2*FONT_SIZE)
    draw_text(screen, time_str, TEXT_FONT, WHITE, 10, 10 + 3*FONT_SIZE)

    pygame.display.flip()

    # pygame.time.delay(framestep)
    dt = clock.tick(FRAMERATE)
    time_elapsed += dt


print(system.balls[0].L)
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
                  "time": "s",
                  "ang_mom": "kg*m^2/s"},
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

questions:
is there a way to predict how long until a system stabilizes?
why are stable orbits not forming anymore after I made changes to
angular momentum, now they just swing apart
is it possible to do advanced stuff like galaxy stuff in pygame
what to do about velocity error
'''