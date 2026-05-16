"""
Function: circulation
Description: Calculates the total bound circulation around the airfoil by 
             performing a numerical line integral of the velocity field.
Inputs:
    - U: Freestream velocity
    - alpha: Angle of attack (degrees)
    - theta_v: Discretized chord angles
    - A0, A1, A2: Fourier coefficients
    - R: Radius of the circular integration contour (default = 2.0)
    - N: Number of points along the circular path
Outputs:
    - Gamma: Absolute value of the total circulation
Assumptions:
    - The circular contour fully encloses the airfoil chord (0 to 1).
    - Velocity is sampled at discrete points on the circle.
"""
import numpy as np
from velocity_field import velocity_field

def circulation(U, alpha, theta_v, A0, A1, A2, R=2.0, N=1000):
    # Define angular segments for the circular path 
    theta_loop = np.linspace(0, 2 * np.pi, N)
    dtheta = 2 * np.pi / N
    
    # Coordinates of the circular path around the airfoil (centered at origin)
    x_c = R * np.cos(theta_loop)
    y_c = R * np.sin(theta_loop)
    
    # Compute differential path vectors (dx, dy) for the integral using the parameterization of the circle
    dx = -R * np.sin(theta_loop) * dtheta
    dy = R * np.cos(theta_loop) * dtheta

    # Extract local velocity components (u, v) at each point on the circle using the velocity field function
    u, v, _, _, _ = velocity_field(x_c, y_c, theta_v, A0, A1, A2, U, alpha)
    
    # Compute tangential velocity component using dot product: Vt = V . dl = u*dx + v*dy
    Vt = u * dx + v * dy
    
    # Sum the components to find total circulation and return the absolute value
    return abs(np.sum(Vt))