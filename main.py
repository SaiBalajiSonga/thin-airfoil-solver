"""
Function: main
Description: The central coordinator for the Thin Airfoil Theory solver. 
             It integrates geometry generation, aerodynamic coefficient 
             calculation, and flow field visualization.
Inputs: None (User provides data via console prompts)
Outputs: Prints Cl, Cm, and Gamma; displays geometric and vector plots.
Assumptions: All required modules (camber, fourier, etc.) are in the same directory.
"""
import numpy as np
from user_input import get_user_input
from camber import camber_line, camber_slope
from fourier import compute_fourier
from velocity_field import mesh_generation, velocity_field, calculate_pressure_distribution
from circulation import circulation
from plotting import plot_camber, plot_slope, plot_vector, plot_gamma_distribution, plot_novel_cambers, plot_pressure_distribution

def main():
    # --- Step 1: Geometry and User Parameters ---
    # choice: Selection between custom or NACA airfoil
    # m: Maximum camber, p: Position of max camber, alpha: Angle of attack
    # U: Freestream velocity, N: Number of discretization points
    choice, m, p, alpha, U, N = get_user_input()

    # x, yc: Chordwise and vertical coordinates of the camber line
    # theta: Angular transformation (0 to pi) for Glauert expansion
    if choice == 3:
        x, yc, theta, yc1, yc2, yc3 = camber_line(choice, m, p, N)
        plot_novel_cambers(x, yc, yc1, yc2, yc3)
        alpha = [-3, 0, 3, 6, 9, 12]
        # xg, yg: 2D meshgrid for the flow domain (4c x 3c)
        xg, yg = mesh_generation()
        #slopes
        s1, s2, s3 = camber_slope(choice, m, p, x)
        for j in range(4):
            if j == 0 :
                y = yc
                slope = camber_slope(2, m, p, x)
            elif j==1:
                y,slope = yc1,s1
            elif j==2:
                y,slope = yc2,s2
            else:
                y,slope = yc3,s3
            print(f"\n--- Aerodynamic Results for Airfoil {j} ---")
            for i in range(len(alpha)):
                A0, A1, A2, Cl, Cm, Cm_LE = compute_fourier(alpha[i], theta, slope)
                print(f"Angle of Attack: {alpha[i]} degrees -> Cl: {Cl:.4f}, Cm_c/4: {Cm:.4f}, Cm_LE: {Cm_LE:.4f}")
                if alpha[i] == 3:
                    # u, v: Total velocity components at each grid point
                    # Vm: Magnitude of the local velocity vector
                    u, v, Vm, _, _ = velocity_field(xg, yg, theta, A0, A1, A2, U, alpha[i])

                    # Visualization of the velocity vectors and airfoil
                    if j != 0: plot_vector(xg, yg, u, v, Vm, x, y, l=f"Velocity Vector Field: Airfoil {j}")

    else: 
        x, yc, theta = camber_line(choice, m, p, N)

        # slope: The local derivative dyc/dx at each x location
        slope = camber_slope(choice, m, p, x)

        # Visualization of the airfoil shape and its gradient
        plot_camber(x, yc, m, p)
        plot_slope(x, slope, p)

        # --- Step 2: Aerodynamic Coefficients Calculation ---
        # A0, A1, A2: Glauert Fourier coefficients
        # Cl: Lift coefficient, Cm: Moment coefficient about c/4, Cm_LE: Moment coefficient about LE
        A0, A1, A2, Cl, Cm, Cm_LE = compute_fourier(alpha, theta, slope)
    
        print(f"\n--- Aerodynamic Results ---")
        print(f"A0: {A0:.4f}, A1: {A1:.4f}, A2: {A2:.4f}")
        print(f"Lift Coefficient (Cl): {Cl:.4f}")
        print(f"Moment Coefficient (Cm_c/4): {Cm:.4f}")
        print(f"Moment Coefficient at LE (Cm_LE): {Cm_LE:.4f}")
        # --- Step 3: Flow Field Computation ---
        # xg, yg: 2D meshgrid for the flow domain (4c x 3c)
        xg, yg = mesh_generation()

        # u, v: Total velocity components at each grid point
        # Vm: Magnitude of the local velocity vector
        u, v, Vm, gamma, x_v = velocity_field(xg, yg, theta, A0, A1, A2, U, alpha)

        # Visualization of the velocity vectors and airfoil
        plot_vector(xg, yg, u, v, Vm, x, yc)
        
        # Plot the distribution of bound circulation gamma along the chord
        plot_gamma_distribution(x_v, gamma)

        # --- Step 4: Circulation Verification ---
        dx_v = np.diff(0.5 * (1 - np.cos(theta)))  # dx_v represents the width of each chord segment

        # By integrating circulation distribution along the chord 
        Gamma_integrated = np.sum(gamma * dx_v)
        # Gamma: Velocity Line Integral around the airfoil using the circulation function
        
        Gamma = circulation(U, alpha, theta, A0, A1, A2)

        print(f"Total Circulation (Integrated Circulation Distribution): {Gamma_integrated:.4f}")
        print(f"Total Circulation (Velocity Line Integral): {Gamma:.4f}")


        # --- Bonus Section 7.1 & 7.2 ---
        # Calculate Cp
        cp_upper, cp_lower = calculate_pressure_distribution(U, gamma)
        # Plot pressure and slope for comparison
        plot_pressure_distribution(x_v, cp_upper, cp_lower, alpha)

        # Numerical Gradient Analysis for the Designer
        # Ignore the first 10% of the chord to avoid the LE singularity and last 10% to avoid the TE where the slope changes rapidly and can cause numerical issues
        check_range = (x_v > 0.10) & (x_v < 0.90)

        max_adverse = float('nan')  # default if check_range is all False
        if np.any(check_range):
            # Only calculate gradient where it's physically meaningful for stall
            # Calculate the rate of change of pressure along the upper surface (dp/dx)
            # In Thin Airfoil Theory, Cp is directly proportional to the vortex strength gamma
            dcp_dx_useful = np.gradient(cp_upper[check_range], x_v[check_range])
            
            # Identify the maximum 'uphill' climb air must make toward the trailing edge
            # High values indicate a risk of boundary layer separation and stall
            max_adverse = np.max(dcp_dx_useful)
            print(f"Max Adverse Pressure Gradient (excluding LE): {max_adverse:.4f}")

        print(f"\n--- Design Diagnostic ---")
        print(f"Max Adverse Pressure Gradient: {max_adverse:.4f}")

        # Heuristic threshold: values > 2.0 suggest the camber curvature is too aggressive
        if not np.isnan(max_adverse) and max_adverse > 2.0: # Threshold for aggressive design {In reality this limit depends on Reynolds number and other factors, but this is a simple heuristic for demonstration}
            # ALERT: If triggered, go to camber.py to reduce 'm' or smooth the custom_airfoil slope
            print("ALERT: High adverse pressure gradient detected. Consider smoothing the camber slope.")
        else:
            # SUCCESS: The pressure recovery is gradual, indicating a robust design for this alpha
            print("SUCCESS: Pressure gradient is within stable limits for design alpha.")

if __name__ == "__main__":
    main()