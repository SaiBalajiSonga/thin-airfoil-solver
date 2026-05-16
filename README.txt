AE 244: Assignment 2 - Thin Airfoil Theory Solver

PROGRAM DESCRIPTION:
   This program analyzes and visualizes the aerodynamic behavior of 2D airfoils using Thin Airfoil Theory. The airfoil is
modeled as a vortex sheet distributed along its mean camber line instead of performing full CFD.

The solver computes aerodynamic coefficients such as Lift Coefficient (Cl) and Moment Coefficient (Cm), calculates the circulation
distribution along the chord, and visualizes the velocity vector field in a 4c x 3c computational domain around the airfoil.

The code also verifies circulation using two methods: 
1. Integrating the vortex strength distribution along the chord 
2. Performing a velocity line integral around a circular contour enclosing the airfoil

INSTRUCTIONS TO RUN THE CODE:
1. Place all project files in the same folder. 
2. Run the program using: python main.py
3. Make a choice for the program: 
   1 -> Custom Camber Airfoil 
   2 -> NACA 4-digit Airfoil 
   3 -> Comparison between NACA airfoil and three novel airfoils
4.  Provide the required inputs:

    -   Maximum camber (m)
    -   Camber position (p)
    -   Angle of attack (alpha in degrees)
    -   Freestream velocity (U in m/s)

CUSTOM AIRFOIL MODIFICATION: 
   Users can test their own airfoil shape by editing the custom camber function:
   * File: camber.py Function: custom_airfoil(x)

   The slope of the camber line will automatically be computed using the numerical_derivative function.

NOVEL AIRFOIL MODIFICATION:
   Users can modify the experimental airfoil designs by editing:
   * File: camber.py Function: Noval_camber_funtions(x)

   These airfoils are used for comparison with the reference NACA airfoil.

EXPECTED OUTPUTS:
   The program prints the following aerodynamic results: 
      - Fourier coefficients (A0, A1, A2) 
      - Lift coefficient (Cl) - Moment coefficient about quarter chord (Cm) 
      - Total circulation using vortex integration 
      - Total circulation using velocity line integral
      - maximum adverse (max(dcp/dx_v))

GENERATED PLOTS:
The solver generates several visualizations:
   1.Camber Line Plot Shows the geometry of the airfoil camber line.
   2.Camber Slope Plot Displays the slope (dyc/dx) distribution along the chord.
   3.Velocity Vector Field Plot Shows airflow around the airfoil in a 4c x 3c domain.
   4.Vortex Strength Distribution Plot Shows the circulation distribution gamma along the chord.
   5.Camber Comparison Plot (for Novel Airfoil Mode) Compares the NACA camber with the three novel airfoil designs.
   6.Pressure distribution curve (cp Vs alpha)

TECHNICAL NOTES: 
- Chord length is normalized to c = 1. 
- Cosine spacing is used to improve leading edge resolution. 
- Midpoint vortex sampling prevents singularities in the velocity calculation. 
- Positive angle of attack produces positive lift.

FILES IN THE PROJECT:
main.py           -> Central program controller 
user_input.py     -> Handles user inputs 
camber.py         -> Camber line generation and slope calculations 
fourier.py        -> Fourier coefficient and aerodynamic calculations 
velocity_field.py -> Velocity field solver using vortex sheet method 
circulation.py    -> Circulation verification using line integral 
plotting.py       -> Plotting and visualization utilities
