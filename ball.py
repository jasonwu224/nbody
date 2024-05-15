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
    
    d -- 3d density
    
    L -- angular momentum (pos -> counterclockwise)'''
    def __init__(self,
                 m: float = 1.,
                 r: tuple[float, float] = (0., 0.), 
                 v: tuple[float, float] = (0., 0.),
                 d: float = 1e9,
                 L: float = 0,
                 dist_scale: float = 1) -> None:
        self.m = float(m)
        self.d = d
        self.r = array(r).astype(float) / dist_scale
        self.v = array(v).astype(float) / dist_scale
        self.L = L
    
    def __str__(self) -> str:
        return f"{self.m} {self.d} {self.r} {self.v}"
    
    def to_dict(self) -> dict:
        return {"m": self.m, 
                "d": self.d, 
                "r": self.r.tolist(), 
                "v": self.v.tolist(),
                "L": self.L}
    
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

    def get_p(self) -> ndarray:
        '''Gets the momentum as a numpy array'''
        return self.m * self.v
    
    def get_I(self) -> float:
        '''Gets the moment of inertia using 2/5 mr^2'''
        # assumes sphere shape
        return 0.4 * self.m * (self.get_radius() ** 2)
    
    def get_omega(self) -> float:
        '''Gets the angular velocity'''
        # L = Iw
        return self.L / self.get_I()

    def get_KE(self) -> float:
        '''Gets the kinetic energy using 0.5mv^2 + 0.5Iw^2'''
        return 0.5 * (self.m * norm(self.v) ** 2 + self.get_I() * self.get_omega() ** 2)
    
    def get_PE(self, other: 'Ball') -> float:
        '''Gets the potential energy using -Gm1m2/r'''
        r = norm(self.r - other.r)
        return -G * self.m * other.m / r
    
    def get_distance_from(self, other: 'Ball') -> float:
        '''Gets the distance from another ball'''
        return norm(self.r - other.r)

    def get_radius(self) -> float:
        '''Calculates ball's radius using its mass and density. Assumes 3d density'''
        volume = self.m / self.d
        # uses V = 4/3 pi r^3
        return cbrt(0.75 * volume / pi)