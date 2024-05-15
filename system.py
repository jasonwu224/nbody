from ball import Ball
from numpy import zeros
from numpy import add
from numpy import cross
from numpy.linalg import norm
from pygame import Rect

class System:
    '''Represents a system of balls
    
    Parameters:

    balls -- list of balls in system
    dist_scale -- ratio of pixel:meter
    time_scale -- ratio of time per frame:dt, where dt is the time
    step for integration and the units for both are milliseconds
    '''
    def __init__(self, balls: list[Ball], dist_scale=1, time_scale=1) -> None:
        self.balls = balls
        self.dist_scale = dist_scale
        self.time_scale = time_scale
    
    def __str__(self) -> str:
        return "\n".join([str(ball) for ball in self.balls])
    
    def to_list(self) -> list:
        return [ball.to_dict() for ball in self.balls]
    
    def update(self, timestep: int) -> None:
        '''Uses semi-implicit euler's method to update velocity and position
        of every ball in the system.
        
        Parameters:
        timestep -- timestep in milliseconds'''
        num_balls = len(self.balls)
        dt = timestep * self.time_scale
        # update velocity
        for i in range(num_balls):
            for j in range(num_balls):
                if i != j:
                    self.balls[i].update_velocity(self.balls[j], dt)
        # update position
        for ball in self.balls:
            ball.update_position(dt)
        # check for collisions
        # could do calculations with velocity but seems more complicated
        # dict is ball eating: ball to remove
        # ideally there should only be one collision ever happening at once
        collision = True
        if collision:
            removed_balls = dict()
            for i in range(num_balls):
                for j in range(i+1, num_balls):
                    ball1 = self.balls[i]
                    ball2 = self.balls[j]
                    if ball1 not in removed_balls and \
                    ball2 not in removed_balls:
                        
                        r = ball1.get_distance_from(ball2)

                        if r < ball1.get_radius() + ball2.get_radius():
                            # remove rect2
                            if ball1.m > ball2.m:
                                removed_balls[ball1] = ball2
                            else:
                                removed_balls[ball2] = ball1
                            # delete after for loops finish
            
            for b1, b2 in removed_balls.items():
                tot_p = b1.get_p() + b2.get_p()
                tot_m = b1.m + b2.m
                final_v = tot_p / tot_m
                final_r = (b1.m * b1.r + b2.m * b2.r) / tot_m
                # conserve angular momentum 
                final_L = cross(b1.r - final_r, b1.get_p()) + \
                        cross(b2.r - final_r, b2.get_p()) + b1.L + b2.L
                b1.L = final_L
                # move position to center of mass
                b1.r = final_r
                # change mass and velocity
                b1.m = tot_m
                b1.v = final_v
                
                # remove could cause conflict if one ball colliding w multiple
                self.balls.remove(b2)

    def get_center_of_mass(self) -> tuple[float, float]:
        '''Returns the coordinate of the center of mass of the system'''
        weighted_position = zeros(self.balls[0].r.shape)
        total_mass = 0

        for ball in self.balls:
            weighted_position += ball.m * ball.r
            total_mass += ball.m
        
        return tuple((1 / total_mass) * self.dist_scale * weighted_position)
    
    def get_info(self) -> tuple:
        '''Returns the tuple pair of total momentum and energy'''
        total_p = zeros(self.balls[0].r.shape)
        total_L = 0  # angular momentum
        total_PE = 0
        total_KE = 0
        num_balls = len(self.balls)
        for i in range(num_balls):
            for j in range(i+1, num_balls):
                total_PE += self.balls[i].get_PE(self.balls[j])
            total_KE += self.balls[i].get_KE() 
            total_p = add(total_p, self.balls[i].get_p())
            # cross of 2d vectors returns scalar
            total_L += cross(self.balls[i].r, self.balls[i].get_p()) + self.balls[i].L
        total_E = total_KE + total_PE
        return norm(total_p), total_L, total_E
