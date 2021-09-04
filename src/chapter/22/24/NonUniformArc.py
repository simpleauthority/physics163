from vpython import *

# Configure the scene
scene.width = 800
scene.height = 600
scene.title = "<h2>Problem 22.24</h2><p>Simulates the electric field at a particular point of interest located at the origin due to a non-uniformly charged arc of radius R.</p><br />"

# Config
pos_color = color.red  # for positive charges, color them red
neg_color = color.blue  # for negative charges, color them blue
scale_factor = 6e4  # arrow scale factor

# Constants
k = 8.99e9  # Coulomb's constant
Q = 500e-9  # total charge, Coulombs (500 nC)
R = 9  # arc radius, meters
N = 200  # number of slices to cut arc into
POI = vec(0, 0, 0)  # electric field point of interest (origin)
theta_min = radians(-45)  # lower end of quarter circle; -45 degrees in radians, wrt y axis
theta_max = radians(45)  # upper end of quarter circle; 45 degrees in radians, wrt y axis
theta_tot = theta_max - theta_min  # 45 - -45 = 90 degrees total arc for quarter circle, wrt y axis
dtheta = theta_tot / N  # angle of each slice of theta total
alpha = (Q * (sqrt(2) + 2)) / 2  # alpha constant
ds = R * dtheta  # arc length of each slice of theta total


# finds the value of lambda and use it to find dq based on the given value of x
def calculate_dq(theta_current):
    # if you're wondering why I called it theta_current it's because pycharm was complaining about name shadowing. whatever
    return (alpha * sin(theta_current)) * ds  # lambda = alpha * sin(theta); dq = lambda * ds


# Coordinate axes
cylinder(pos=vec(-(R + 1), 0, 0), axis=vec(2 * (R + 1), 0, 0), radius=0.05)  # x-axis
cylinder(pos=vec(0, -2, 0), axis=vec(0, 2 + (R + 1), 0), radius=0.05)  # y-axis

# Simulation variables
sphere_min_pos = ds / 2  # minimum value
E_total = vec(0, 0, 0)  # total electric field
arc = []  # collection of charges on arc
dq_min = 0  # min dq seen
dq_max = 0  # max dq seen

# Draw charges and calculate electric field
for theta in arange(theta_min + (dtheta / 2), theta_max, dtheta):  # iterate from start to end by dtheta
    rate(60)

    charge = sphere(pos=vec(R * sin(theta), R * cos(theta), 0), radius=0.25)  # draw charge

    charge.dq = calculate_dq(theta)  # calculate dq

    # record dq_max/dq_min
    if charge.dq > dq_max:
        dq_max = charge.dq
    elif charge.dq < dq_min:
        dq_min = charge.dq

    charge.r = POI - charge.pos  # calculate r from POI to charge

    E_total += (k * charge.dq * charge.r) / pow(mag(charge.r), 3)  # add to electric field

    arc.append(charge)

# Set charge colors
for charge in arc:
    if charge.dq > 0:
        charge.color = vec(0.2 + (0.8 * (charge.dq / dq_max)), 0, 0)  # set red with variable intensity based on charge
    else:
        charge.color = vec(0, 0, 0.2 + (0.8 * (charge.dq / dq_min)))  # set blue with variable intensity based on charge

# Draw POI test charge, calculate force at POI, and draw force arrow
poi_object = sphere(pos=POI, color=pos_color, radius=0.25)
force_poi = Q * E_total
force_poi_arrow = arrow(pos=POI, axis=force_poi * scale_factor, color=color.orange)

# Get experimental results, find the percent difference from theoretical
e_total_mag_ex = mag(E_total)  # experimental electric field mag
e_total_mag_th = mag(vec((-0.2854 * k * alpha) / R, 0, 0))  # theoretical electric field mag
percent_diff = ((e_total_mag_ex - e_total_mag_th) / e_total_mag_th) * 100  # percent difference from theory

# print results
print(f"Total arc length (Θ): {theta_tot:.3f} rad / {degrees(theta_tot):.1f} °")
print(f"Total charge (Q): {Q} C")
print(f"Charge distribution constant (α): {alpha} C/m")
print(f"Experimental electric field magnitude: {e_total_mag_ex:.4f} N/C")
print(f"Theoretical electric field magnitude: {e_total_mag_th:.4f} N/C")
print(f"Experimental percent difference from theory: {percent_diff:.3f}%")
