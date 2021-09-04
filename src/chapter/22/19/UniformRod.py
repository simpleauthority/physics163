from vpython import *

# Configure the scene
scene.width = 800
scene.height = 600
scene.title = "<h2>Problem 22.19</h2><p>Simulates the electric field at a particular point of interest due to an uniformly charged rod of length L located at the origin.</p><p>Solution to theoretical electric field: <a href='https://bit.ly/3n3B7pg' target='_blank'>https://bit.ly/3n3B7pg</a></p><br />"

# Config
pos_color = color.red  # for positive charges, color them red
neg_color = color.blue  # for negative charges, color them blue
scale_factor = 1e5  # arrow scale factor

# Constants
k = 8.99e9  # Coulomb's constant
Q = 500e-9  # total charge, Coulombs (500 nC)
L = 5       # rod length, meters
POI = vec(0, L, 0)  # electric field point of interest
N = 10  # number of slices to cut rod into
lam = Q/L  # charge density
dx = L/N  # length of each dq
dq = lam * dx  # charge differential per slice

# Coordinate axes
cylinder(pos=vec(-1, 0, 0), axis=vec(L + 2, 0, 0), radius=0.05)  # x-axis
cylinder(pos=vec(0, -1, 0), axis=vec(0, L + 3, 0), radius=0.05)  # y-axis

# Draw the rod
cylinder(pos=vec(0, 0, 0), axis=vec(L, 0, 0), radius=0.2, opacity=0.5)

# Simulation variables
x_min = dx / 2  # minimum x value
x_max = x_min + L
E_total = vec(0, 0, 0)  # total electric field

# Draw charges and calculate electric field
for x in arange(x_min, x_max, dx):  # iterate from x_min to x_max by dx
    charge = sphere(pos=vec(x, 0, 0), radius=0.25, color=pos_color if dq > 0 else neg_color)  # draw charge
    charge.r = POI - charge.pos  # calculate r from POI to charge
    E_total += (k * dq * charge.r) / pow(mag(charge.r), 3)  # add to electric field

# Draw POI test charge, calculate force at POI, and draw force arrow
poi_object = sphere(pos=POI, color=pos_color, radius=0.25)
force_poi = Q * E_total
force_poi_arrow = arrow(pos=POI, axis=force_poi*scale_factor, color=color.orange)

# Get experimental results, find the percent difference from theoretical
e_total_mag_ex = mag(E_total)  # experimental electric field mag
e_total_mag_th = mag(vec(((k * Q * (1 - sqrt(2))) / (pow(L, 2) * sqrt(2))), ((k * Q) / (pow(L, 2) * sqrt(2))), 0))  # theoretical electric field mag (solution: https://bit.ly/3n3B7pg)
percent_diff = ((e_total_mag_ex - e_total_mag_th) / e_total_mag_th) * 100  # percent difference from theory

# print results
print(f"Rod length (L): {L:.2f} m")
print(f"Total charge (Q): {Q} C")
print(f"Charge distribution (λ): {lam} C/m")
print(f"Experimental electric field magnitude: {e_total_mag_ex:.4f} N/C")
print(f"Theoretical electric field magnitude: {e_total_mag_th:.4f} N/C")
print(f"Experimental percent difference from theory: {percent_diff:.3f}%")
