from vpython import *

# Configure the scene
scene.width = 800
scene.height = 600
scene.title = "<h2>Problem 22.23</h2><p>Simulates the electric field at a particular point of interest located at the origin due to a uniformly charged arc of radius R.</p><br />"

# Config
pos_color = color.red  # for positive charges, color them red
neg_color = color.blue  # for negative charges, color them blue
scale_factor = 3e5  # arrow scale factor

# Constants
k = 8.99e9  # Coulomb's constant
Q = 500e-9  # total charge, Coulombs (500 nC)
R = 9       # arc radius, meters
N = 200  # number of slices to cut arc into
POI = vec(0, 0, 0)  # electric field point of interest (origin)
theta_min = radians(-45)  # lower end of quarter circle; -45 degrees in radians, wrt y axis
theta_max = radians(45)  # upper end of quarter circle; 45 degrees in radians, wrt y axis
theta_tot = theta_max - theta_min  # 45 - -45 = 90 degrees total arc for quarter circle, wrt y axis
dtheta = theta_tot / N  # angle of each slice of theta total
lam = Q/(R*theta_tot)  # charge density for entire arc length
ds = R * dtheta  # arc length of each slice of theta total
dq = lam * ds  # charge differential per arc slice

# Coordinate axes
cylinder(pos=vec(-(R + 1), 0, 0), axis=vec(2 * (R + 1), 0, 0), radius=0.05)  # x-axis
cylinder(pos=vec(0, -2, 0), axis=vec(0, 2 + (R + 1), 0), radius=0.05)  # y-axis

# Simulation variables
sphere_min_pos = ds / 2  # minimum value
E_total = vec(0, 0, 0)  # total electric field

# Draw charges and calculate electric field
for theta in arange(theta_min + (dtheta / 2), theta_max, dtheta):  # iterate from start to end by dtheta
    rate(60)
    charge = sphere(pos=vec(R*sin(theta), R*cos(theta), 0), radius=0.25, color=pos_color if dq > 0 else neg_color)  # draw charge
    charge.r = POI - charge.pos  # calculate r from POI to charge
    E_total += (k * dq * charge.r) / pow(mag(charge.r), 3)  # add to electric field

# Draw POI test charge, calculate force at POI, and draw force arrow
poi_object = sphere(pos=POI, color=pos_color, radius=0.25)
force_poi = Q * E_total
force_poi_arrow = arrow(pos=POI, axis=force_poi*scale_factor, color=color.orange)

# Get experimental results, find the percent difference from theoretical
e_total_mag_ex = mag(E_total)  # experimental electric field mag
e_total_mag_th = mag(vec(0, (-0.9003*k*Q)/(R**2), 0))  # theoretical electric field mag
percent_diff = ((e_total_mag_ex - e_total_mag_th) / e_total_mag_th) * 100  # percent difference from theory

# print results
print(f"Total arc length (Θ): {theta_tot:.3f} rad / {degrees(theta_tot):.1f} °")
print(f"Total charge (Q): {Q} C")
print(f"Charge distribution (λ): {lam:.4e} C/m")
print(f"Experimental electric field magnitude: {e_total_mag_ex:.4f} N/C")
print(f"Theoretical electric field magnitude: {e_total_mag_th:.4f} N/C")
print(f"Experimental percent difference from theory: {percent_diff:.3f}%")
