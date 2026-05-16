"""
Function: plot_camber, plot_novel_cambers, plot_slope, plot_vector, plot_gamma_distribution
Description: A complete visualization toolkit for Thin Airfoil Theory, 
             mapping geometric curvature to aerodynamic response.
Inputs:
    - Geometry arrays (x, yc, slope)
    - Vector field arrays (xg, yg, u, v, Vm)
    - Vortex strength (gamma)
Outputs:
    - Matplotlib figures and axes
"""
import matplotlib.pyplot as plt

def plot_camber(x, yc, m=0, p=0):

    plt.figure(figsize=(10, 4)) # Initialize a new figure with a wide aspect ratio for the airfoil profile
    plt.plot(x, yc, label="Camber Line") # Plot the vertical camber coordinates (yc) against the chordwise position (x)
    
    # Check if the maximum camber (m) is non-zero to avoid marking flat plates
    if m > 0:
        # Highlight the specific point of maximum camber for NACA geometric reference
        plt.scatter(p, m, color='red', label="Maximum Camber Location")
    
    plt.xlim(0, 1) # Restrict the x-axis to the physical length of the chord (0 to 1)

    # Assign descriptive labels to the axes using non-dimensional units
    plt.xlabel("Chord position (x/c)")
    plt.ylabel("Camber (yc/c)")
    
    plt.grid(True) # Enable grid lines to help visualize the curvature magnitude
    plt.legend()  # Display the legend to identify the camber line and max point
    plt.title("Airfoil Camber Line") # Set the plot title for clear identification
    plt.axis("equal") # Force equal scaling so the airfoil geometry isn't visually stretched
    plt.tight_layout() # Adjust subplot parameters to give the plot more breathing room
    plt.show() # Render the final plot to the screen


def plot_novel_cambers(x, yc, yc1, yc2, yc3):

    plt.figure(figsize=(10, 4)) # Create a figure suitable for comparing multiple geometric profiles
    
    # Plots the Camber lines of 3 Novel airfoils and NACA airfoil
    plt.plot(x, yc, label="NACA Airfoil")
    plt.plot(x, yc1, label="Airfoil 1")
    plt.plot(x, yc2, label="Airfoil 2")
    plt.plot(x, yc3, label="Airfoil 3")
    
    plt.xlim(0, 1) # Fix the x-axis range to represent the standard chord length
    
    # Label axes to indicate chordwise position and vertical displacement
    plt.xlabel("Chord position (x/c)")
    plt.ylabel("Camber (yc/c)")
    
    
    plt.grid(True) # Add grid lines to enhance visibility of curvature differences between airfoils
    plt.legend() # Include a legend to differentiate between the four plotted airfoils    
    plt.title("Comparison of Novel Airfoil Camber Lines") # Set a title that reflects the comparative nature of the plot
    plt.axis("equal") # Ensure geometry is shown in a 1:1 ratio to maintain physical accuracy
    plt.tight_layout() # Optimize layout to prevent label clipping
    plt.show() # Display the comparison plot

def plot_slope(x, slope, p):
    plt.figure(figsize=(10, 4)) # Initialize a figure to visualize the first derivative of the camber line
    
    # Plot the local slope (gradient) across the chord to see curvature changes
    plt.plot(x, slope)
    
    # Label the axes to indicate chordwise position and slope magnitude
    plt.xlabel("Chord position (x/c)")
    plt.ylabel("Slope (dyc/dx)")
    
    plt.title("Camber Line Slope") # Title the plot to indicate it represents the geometric gradient
    plt.grid(True) # Apply a grid for easier reading of slope values at specific x-positions
    plt.tight_layout() # Apply automatic padding adjustments
    plt.show() # Render the slope distribution plot

def plot_vector(xg, yg, u, v, Vm, x_camber, y_camber, l = "Velocity Vector Field (Thin Airfoil Theory)"):
    
    plt.figure(figsize=(10, 6)) # Create a large figure to accommodate the vector field and colorbar
    
    # Plot velocity vectors at each grid point; color represents magnitude of velocity
    q = plt.quiver(xg, yg, u, v, Vm, cmap="jet")
    
    # Add scale for velocity magnitude and colorbar for reference
    plt.colorbar(q, label="Velocity Magnitude")
    
    # Overlay the physical airfoil geometry for reference
    plt.plot(x_camber, y_camber, color='black', linewidth=2, label="Airfoil")
    
    # adding labels to axes
    plt.xlabel("X/c")
    plt.ylabel("Y/c")
    
    # Define domain size: 4c along x and 3c along y 
    plt.xlim(-1.5, 2.5) 
    plt.ylim(-1, 2)
    
    # Ensure 1 unit on X is the same as 1 unit on Y to prevent distortion 
    plt.gca().set_aspect('equal') 
    
    plt.title(l) #Adding Title
    plt.tight_layout() # Does automatic padding
    plt.show() #shows plot

def plot_gamma_distribution(x_v, gamma):
    # Set up a figure to visualize the circulation/vortex strength
    plt.figure(figsize=(8, 5))
    
    # Plot the vortex strength distribution using a solid blue line
    plt.plot(x_v, gamma, 'b-', linewidth=2, label=r'$\gamma(\theta)$')
    
    # Use LaTeX formatting for professional-grade axis labels
    plt.xlabel('Chordwise Position, x/c')
    plt.ylabel(r'Vortex Strength, $\gamma(\theta)$ [m/s]') 
    
    # Title the plot to clarify what the vortex distribution represents
    plt.title("Vortex Strength Distribution along Chord")
    
    plt.grid(True, linestyle='--', alpha=0.5)  # Apply a light dashed grid to help identify the Kutta condition at the trailing edge
    plt.legend() # Display the label identifying the plotted function

    # Set x-limits slightly outside [0, 1] to see the leading and trailing edge behavior
    plt.xlim([-0.1, 1]) 
    
    # Dynamically scale the y-axis based on the maximum vortex strength found
    plt.ylim([-250, max(gamma)*1.1]) 
    
    plt.tight_layout() # Minimize white space around the plot
    plt.show() # Display the distribution plot


def plot_pressure_distribution(x_v, cp_upper, cp_lower, alpha):
    plt.figure(figsize=(10, 6)) # Set figure size
    # Plot Cp distribution for upper and lower surfaces; color-code for clarity
    plt.plot(x_v, cp_upper, 'r-', label='Upper Surface')
    plt.plot(x_v, cp_lower, 'b-', label='Lower Surface')
    plt.gca().invert_yaxis()  # Standard convention: -Cp is upwards
    plt.xlim(-0.0001, 1) # Focus on the chord length
    plt.ylim(2, -2) # Zooms in on the typical range of Cp values for better visibility of pressure differences
    # adding labels to axes
    plt.xlabel('Chordwise Position (x/c)')
    plt.ylabel('Pressure Coefficient (Cp)')

    plt.title(f'Pressure Distribution at alpha = {alpha}°') # Title with angle of attack for context
    plt.legend() # Display the legend to differentiate between upper and lower surface Cp
    plt.grid(True, linestyle='--') #adding grid
    plt.tight_layout() # Adjust layout to prevent clipping of labels and title
    plt.show()