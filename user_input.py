"""
Function: get_user_input
Description: Interactively collects airfoil geometry and flight parameters.
Inputs: None (User keyboard input).
Outputs: 
    - choice: Int (1: Custom, 2: NACA, 3: Novel Comparison).
    - m: Float (Max camber height).
    - p: Float (Max camber position).
    - alpha: Float or List (Angle of attack in degrees).
    - U: Float (Freestream velocity).
    - N: Int (Points for discretization).
Assumptions: User provides numeric values within realistic aerodynamic ranges.
"""
import numpy as np

def get_user_input():
    # Selection menu for airfoil type 
    print("Select Camber Type")
    print("1 -> Custom Camber")
    print("2 -> NACA Camber")
    print("3 -> Novel Airfoil Comparison (Section 4 Tasks)")

    choice = int(input("Enter choice: ")) # User's selection code

    # Input handling for NACA geometry parameters 
    if choice != 1:
        m = float(input("Enter maximum camber, M [m]: ")) # Height of max camber 
        p = float(input("Enter maximum camber position, P [m]: ")) # Position of max camber 
    else:
        # Default placeholders for custom airfoil
        m = 0
        p = 0

    # Flight condition inputs 
    alpha = 0.0 # Initializing AoA variable
    if choice != 3:
        alpha = float(input("Enter angle of attack, \u03B1 [°]: ")) # Single AoA for standard runs
    
    U = float(input("Enter freestream velocity, U [m/s]: ")) # Airspeed magnitude (e.g., 20 m/s)
    N = int(input("Enter number of discretization points (e.g., 1000): ")) # Points along chord

    return choice, m, p, alpha, U, N