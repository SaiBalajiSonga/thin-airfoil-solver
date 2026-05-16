"""
Function: compute_fourier
Description: Solves for the Glauert Fourier coefficients (A0, A1, A2) using the 
             Thin Airfoil Theory fundamental equation and trapezoidal integration.
Inputs:
    - alpha: Angle of attack in degrees
    - theta: Angular coordinates (0 to pi)
    - slope: Camber line slope dyc/dx corresponding to theta
Outputs:
    - A0, A1, A2: First three Fourier coefficients
    - Cl: Lift Coefficient
    - Cm: Moment Coefficient about the quarter-chord
Assumptions:
    - Small angle approximation (sin alpha ~ alpha)
    - Kutta condition is satisfied at the trailing edge.
"""
import numpy as np

def compute_fourier(alpha, theta, slope):
    alpha_rad = np.deg2rad(alpha) # Convert input AoA to radians

    # Perform numerical integration for Fourier Coefficients
    # A0 represents the angle of attack and mean slope effect
    A0 = alpha_rad - (1/np.pi) * np.trapezoid(slope, theta)
    
    # A1 and A2 capture the camber shape distribution
    A1 = (2/np.pi) * np.trapezoid(slope * np.cos(theta), theta)
    A2 = (2/np.pi) * np.trapezoid(slope * np.cos(2 * theta), theta)

    # Final Aerodynamic Coefficients
    Cl = np.pi * (2 * A0 + A1) # Theoretical Lift Coefficient
    Cm = -(np.pi / 4) * (A1 - A2) # Theoretical Moment Coefficient (c/4)
    Cm_LE = - (np.pi / 2)*(A0 + A1 - (A2/2))# Moment Coefficient at the trailing edge (for Kutta condition verification)
    return A0, A1, A2, Cl, Cm, Cm_LE   # Returns the values when the funtion is called