from vpython import *

# Configure the scene
scene.width = 1024
scene.height = 720
scene.background = vec(1, 1, 1)
scene.title = "<h2>Map of Electric Potential</h2><p>Simulates a map of electric potential as caused by two point charges in space.</p><br />"


# Config
pos_color = color.red  # for positive charges, color them red
neg_color = color.blue  # for negative charges, color them blue


# Functions to use later
def draw_charge(name, value, pos):
    charge = sphere(pos=pos, radius=0.6, color=pos_color if value > 0 else neg_color)
    charge.label = label(pos=pos + vec(0, charge.radius / 2, 0), text=f"{name}\n{value:.1e}", height=11, box=False, opacity=0, color=color.white)
    return charge


# Constants
k = 8.99e9  # Coulomb's constant
q1 = -10.0e-9  # charge 1, -10 nC
q2 = 10.0e-9  # charge 2, +10 nC
x_min = -8
x_max = 8
dx = 0.25
y_min = -8
y_max = 8
dy = 0.25

# Draw coordinate axes
x_axis = cylinder(pos=vec(x_min, 0, 0), axis=vec(2 * x_max, 0, 0), radius=0.05)  # x-axis
label(pos=x_axis.pos + x_axis.axis + vec(0.5, 0, 0), text="X", box=False, opacity=1)
y_axis = cylinder(pos=vec(0, y_min, 0), axis=vec(0, 2 * y_max, 0), radius=0.05)  # y-axis
label(pos=y_axis.pos + y_axis.axis + vec(0, 0.5, 0), text="Y", box=False, opacity=1)

# Draw physical charges
q1_sphere = draw_charge(name="q1", value=q1, pos=vec(3, 3, 0))
q2_sphere = draw_charge(name="q2", value=q2, pos=vec(-3, -3, 0))

# Create graph
x_potential = graph(width=1024, height=225,
                               title="<b><i>x</i> (m) vs <i>potential</i> (V)</b>",
                               xtitle="<i>x</i> (m)", ytitle="<i>potential</i> (V)",
                               foreground=vec(0, 0, 0), background=vec(1, 1, 1))

# Create a curve for plotting on the graph
x_potential_curve = gcurve(color=vec(0, 0.4, 1))

# Simulation variables
V_max = 15

print("Drawing the electric potential grids...")

# Draw electric field arrows at every y in y_min to y_max by dy
# for every x in x_min to x_max by dx
for x in arange(x_min, x_max + dx, dx):
    for y in arange(y_min, y_max + dy, dy):
        # print(f"Drawing potential at ({x}, {y})")
        rate(240)

        # Declare the POI, which is every point
        # (dx, dy) visited by the loop
        point_of_interest = vec(x, y, 0)

        # Create potential grid
        grid = box(pos=point_of_interest, size=vec(dx, dy, 0))

        # Find r-vectors from POI to each charge
        r1 = point_of_interest - q1_sphere.pos
        r2 = point_of_interest - q2_sphere.pos

        if mag(r1) == 0 or mag(r2) == 0:
            # if the POI is directly on top of a charge, the voltage becomes infinite - we ignore it
            V = 0
        else:
            # we create the net electric potential at this POI by summing the individual potentials created by each charge
            V = ((k * q1) / mag(r1)) + ((k * q2) / mag(r2))

        # Set the color of the grid based on resulting potential
        if V >= 0:
            grid.color = pos_color
        else:
            grid.color = neg_color

        # Determine opacity of grid based on if it is greater than V_max or smaller than -V_max
        if V > V_max:
            grid.opacity = 1
        elif V < -V_max:
            grid.opacity = 1
        else:
            grid.opacity = abs(V)/V_max

        x_potential_curve.plot(x, V)

print("The electric potential grids have been drawn.")
