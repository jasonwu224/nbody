from numpy import array, cbrt
from numpy import ndarray
from numpy.linalg import norm
from scipy.constants import G, pi

class Ball:
    '''A class representing a ball with mass, position, velocity, and
    contains its surface. 

    TODO:
    add a field for the distance unit per pixel, rn it's
    default meters

    Parameters:

    m -- mass in kg

    r -- initial position vector where origin is top left
         type tuple of floats, default (0, 0)

    v -- initial velocity vector
         type tuple of floats, default (0, 0)'''

    '''Constructor for a Ball

    Parameters:

    m -- mass in kg

    r -- initial position vector where origin is top left
         type tuple of floats, default (0, 0)

    v -- initial velocity vector
         type tuple of floats, default (0, 0)
    
    d -- 2d density (might change to 3d)'''
    def __init__(self,
                 m: float = 1.,
                 r: tuple[float, float] = (0., 0.), 
                 v: tuple[float, float] = (0., 0.),
                 d: float = 1e9) -> None:
        self.m = float(m)
        self.density = d
        self.r = array(r).astype(float)
        self.v = array(v).astype(float)
    
    def __str__(self) -> str:
        return f"{self.m} {self.density} {self.r} {self.v}"
    
    def to_dict(self) -> dict:
        return {"m": self.m, 
                "density": self.density, 
                "r": self.r.tolist(), 
                "v": self.v.tolist()}
    
    def update_velocity(self, other: 'Ball', timestep: int) -> None:
        '''Updates velocity using gravitational force of another ball and 
        a timestep. 
        
        Parameters:

        other -- the other ball

        timestep -- the timestep in milliseconds'''
        # convert from milliseconds to seconds
        delta_t = timestep / 1000
        # F_21 = -((Gm1m2)/|r_21|^3)r_21
        # r_21 = r2 - r1, F_21 is force of 1 on 2
        r = self.r - other.r
        a = (-G * other.m / (norm(r) ** 3)) * r
        # update velocity
        self.v += a * delta_t
    
    def update_position(self, timestep: int) -> None:
        '''Updates position using velocity and timestep.
        
        Parameters:

        timestep -- the timestep in milliseconds'''
        delta_t = timestep / 1000
        self.r += self.v * delta_t
    
    def get_momentum(self) -> ndarray:
        '''Gets the momentum as a numpy array'''
        return self.m * self.v

    def get_KE(self) -> float:
        '''Gets the kinetic energy using 0.5mv^2'''
        return 0.5 * self.m * norm(self.v) ** 2
    
    def get_PE(self, other: 'Ball') -> float:
        '''Gets the potential energy using -Gm1m2/r'''
        r = norm(self.r - other.r)
        return -G * self.m * other.m / r
    
    def get_distance_from(self, other: 'Ball') -> float:
        '''Gets the distance from another ball'''
        return norm(self.r - other.r)

    def get_radius(self) -> float:
        '''Calculates ball's radius using its mass and density. Assumes 3d density'''
        volume = self.m / self.density
        # uses V = 4/3 pi r^3
        return cbrt(0.75 * volume / pi)