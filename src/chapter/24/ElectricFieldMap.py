from vpython import *

# Configure the scene
scene.width = 1024
scene.height = 720
scene.background = vec(1, 1, 1)
scene.title = "<h2>Map of Electric Field Arrows</h2><p>Simulates a map of electric field arrows as caused by two point charges in space.</p><br />"

# Config
pos_color = color.red  # for positive charges, color them red
neg_color = color.blue  # for negative charges, color them blue
scale_factor = 0.7  # how much to scale each arrow
sat_level = 1  # arrow saturation level (max size of arrow)


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

# Simulation variables
E_min = 0
E_max = 0

print("Drawing the electric field arrows...")

# Draw electric field arrows at every y in y_min to y_max + dy by dy
# for every x in x_min - dx to x_max by dx
for x in arange(x_min, x_max + dx, dx):
    for y in arange(y_min, y_max + dy, dy):
        # print(f"Drawing arrow at ({x}, {y})")
        rate(240)

        # Declare the POI, which is every point
        # (dx, dy) visited by the loop
        point_of_interest = vec(x, y, 0)

        # Find r-vectors from POI to each charge
        r1 = point_of_interest - q1_sphere.pos
        r2 = point_of_interest - q2_sphere.pos

        if mag(r1) == 0 or mag(r2) == 0:
            # if the POI is directly on top of a charge, the field becomes infinite - we ignore it
            E = vec(0, 0, 0)
        else:
            # we create the net electric field at this POI by summing the individual fields created by each charge
            E = ((k * q1 * r1) / (mag(r1) ** 3)) + ((k * q2 * r2) / (mag(r2) ** 3))

        # Get the magnitude of the electric field at this POI
        E_mag = mag(E)

        # Determine if the electric field would be larger than the saturation level
        if E_mag > sat_level:
            # If so, resize it to the saturation level
            E = sat_level * hat(E)
            E_mag = mag(E)

        # Create an arrow for the electric field at this POI
        E_arrow = arrow(pos=point_of_interest, axis=E * scale_factor, color=color.white)

        # Determine if the E_mag is the new E_max or E_min
        if E_mag > E_max:
            E_max = E_mag
        elif E_mag < E_min:
            E_min = E_mag

        # Change the arrow opacity based on strength of the electric field at this POI
        if E_mag > 0:
            E_arrow.opacity = E_mag/E_max
        elif E_mag < 0:
            E_arrow.opacity = E_mag/E_min

print("The electric field arrows have been drawn.")
