from vpython import *

# Configure the scene
scene.width = 800
scene.height = 600
scene.title = "<h2>Problem 22.14</h2><p>Simulates the electric field at a particular point of interest due to non-uniformly charged rod of length L centered on the origin.</p><br />"

# Config
pos_color = color.red  # for positive charges, color them red
neg_color = color.blue  # for negative charges, color them blue
scale_factor = 1e5  # arrow scale factor

# Constants
k = 8.99e9  # Coulomb's constant
Q = 500e-9  # total charge, Coulombs (500 nC)
L = 12  # rod length, meters
y = 5  # POI position on y-axis
POI = vec(0, y, 0)  # electric field point of interest
N = 10  # number of slices to cut rod into
alpha = (12 * Q) / pow(L, 3)  # alpha constant
dx = L / N  # length of each dq


# finds the value of lambda and use it to find dq based on the given value of x
def calculate_dq(x_pos):
    # if you're wondering why I called it x_pos it's because pycharm was complaining about name shadowing. whatever
    return (alpha * pow(x_pos, 2)) * dx  # lambda = alpha * x^2; dq = lambda * dx


# Coordinate axes
cylinder(pos=vec(-8, 0, 0), axis=vec(16, 0, 0), radius=0.05)  # x-axis
cylinder(pos=vec(0, -2, 0), axis=vec(0, 8, 0), radius=0.05)  # y-axis

# Draw the rod
cylinder(pos=vec((-L) / 2, 0, 0), axis=vec(2 * (L / 2), 0, 0), radius=0.2, opacity=0.5)

# Simulation variables
x_min = ((-L) / 2) + (dx / 2)  # minimum x value
x_max = x_min + L  # maximum x value
E_total = vec(0, 0, 0)  # total electric field
rod = []  # collection of all charges on rod
dq_min = 0  # minimum dq encountered
dq_max = 0  # maximum dq encountered

# Draw charges and calculate electric field
for x in arange(x_min, x_max, dx):  # iterate from x_min to x_max by dx
    charge = sphere(pos=vec(x, 0, 0), radius=0.25)  # draw charge

    charge.dq = calculate_dq(x)  # calculate dq

    if charge.dq > dq_max:
        dq_max = charge.dq
    elif charge.dq < dq_min:
        dq_min = charge.dq

    charge.r = POI - charge.pos  # calculate r from POI to charge

    E_total += (k * charge.dq * charge.r) / pow(mag(charge.r), 3)  # add to electric field

    rod.append(charge)

# Set charge colors
for charge in rod:
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
e_total_mag_th = mag(vec(0, ((k * y * alpha) * ((y*sqrt(((L**2)/(4*y**2)) + 1)*(log(sqrt(((L**2)/(4*y**2)) + 1) + L/(2*y))-log(sqrt(((L**2)/(4*y**2)) + 1) - L/(2*y)))-L)/sqrt(((L**2)/4) + y**2))), 0))  # theoretical electric field mag
percent_diff = ((e_total_mag_ex - e_total_mag_th) / e_total_mag_th) * 100  # percent difference from theory

# print results
print(f"Experimental electric field magnitude: {e_total_mag_ex:.4f} N/C")
print(f"Theoretical electric field magnitude: {e_total_mag_th:.4f} N/C")
print(f"Experimental percent difference from theory: {percent_diff:.4f}%")
