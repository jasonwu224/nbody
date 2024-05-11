from ball import Ball
from numpy import zeros
from numpy import add
from numpy.linalg import norm
from pygame import Rect

class System:
    '''Represents a system of balls'''

    def __init__(self, balls: list[Ball]) -> None:
        self.balls = balls
    
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
        # update velocity
        for i in range(num_balls):
            for j in range(num_balls):
                if i != j:
                    self.balls[i].update_velocity(self.balls[j], timestep)
        # update position
        for ball in self.balls:
            ball.update_position(timestep)
        # check for collisions
        # could do calculations with velocity but seems more complicated
        # dict is ball eating: ball to remove
        # ideally there should only be one collision ever happening at once
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
            tot_p = b1.get_momentum() + b2.get_momentum()
            tot_m = b1.m + b2.m
            final_v = tot_p / tot_m

            b1.m = tot_m
            b1.v = final_v
            # remove could cause conflict if one ball colliding w multiple
            self.balls.remove(b2)
    
    # def get_positions(self) -> tuple[tuple[Ball, tuple[float, float]], ...]:
    #     '''Returns a tuple of pairs (Ball object, Ball coordinate)'''
    #     return ((ball.surface, ball.r) for ball in self.balls)

    def get_center_of_mass(self) -> tuple[float, float]:
        '''Returns the coordinate of the center of mass of the system'''
        weighted_position = zeros(self.balls[0].r.shape)
        total_mass = 0

        for ball in self.balls:
            weighted_position += ball.m * ball.r
            total_mass += ball.m
        
        return tuple((1 / total_mass) * weighted_position)
    
    def get_info(self) -> tuple:
        '''Returns the tuple pair of total momentum and energy'''
        total_p = zeros(self.balls[0].r.shape)
        total_E = 0
        num_balls = len(self.balls)
        for i in range(num_balls):
            for j in range(i+1, num_balls):
                total_E += self.balls[i].get_PE(self.balls[j])
            total_E += self.balls[i].get_KE()
            total_p = add(total_p, self.balls[i].get_momentum())
        
        return norm(total_p), total_E
