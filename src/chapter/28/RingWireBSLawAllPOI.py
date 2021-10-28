from vpython import *

# constants
ring_radius = 0.105  # radius of ring, meters
num_slices = 360  # how many slices to cut ring into; num slices 360 causes huge pdiff why?
theta_min = 0  # min angle of ring, radians
theta_max = 2 * pi  # max angle of ring, radians
total_theta = theta_max - theta_min  # total angle of ring, radians
dtheta = total_theta / num_slices  # differential angle of each slice, radians

mu_naught = (4 * pi) * 1e-7  # tesla*meter/sec
current = 300.0  # amps
integration_constant = (mu_naught * current) / (4 * pi)  # constant out front of BS law integral

scale_factor = 2e-14  # factor by which to scale arrows

# axes
line_x = cylinder(pos=vec(-0.15, 0, 0), axis=vec(0.30, 0, 0), radius=0.0005)
line_y = cylinder(pos=vec(0, -0.15, 0), axis=vec(0, 0.30, 0), radius=0.0005)
line_z = cylinder(pos=vec(0, 0, -0.15), axis=vec(0, 0, 0.30), radius=0.0005)
label_x = label(pos=line_x.pos + line_x.axis, text='x', height=10)  # set axes labels
label_y = label(pos=line_y.pos + line_y.axis, text='y', height=10)
label_z = label(pos=line_z.pos + line_z.axis, text='z', height=10)


# get direction of any theta position on the ring
def calc_theta_hat(theta):
    return vec(0, cos(theta), -sin(theta))  # yz plane, x set to zero


# get differential arclength of ring
def calc_ds(theta):
    return ring_radius * dtheta * calc_theta_hat(theta)


# calculate the magnetic field of the ring at a specific position
def calc_mag_field(position):
    B_total = vec(0, 0, 0)  # total magnetic field

    for theta in arange(theta_min, theta_max, dtheta):
        segment = ring_radius * vec(0, sin(theta), cos(theta))
        r = position - segment  # r vector from segment to arbitrary POI --ring in yz plane--
        r_mag = mag(r)  # mag of r vector

        ds = calc_ds(theta)  # differential arclength of a specific theta

        if r_mag != 0:
            B_total += integration_constant * (cross(ds, r) / r_mag ** 3)  # append differential B to total B

    return B_total


# draw ring
ring = ring(pos=vec(0, 0, 0), axis=vec(1, 0, 0), radius=ring_radius, thickness=0.005)

# draw pois and calc data for every point in space
x_min = y_min = z_min = -0.15
x_max = y_max = z_max = 0.30
dx = dy = dz = 0.05

for x in arange(x_min, x_max, dx):
    for y in arange(y_min, y_max, dy):
        for z in arange(z_min, z_max, dz):
            poi = vec(x, y, z)

            exp_b = calc_mag_field(poi)
            print(f"exp b at ({x}, {y}, {z}): {mag(exp_b)}")

            b_arrow = arrow(pos=poi, axis=exp_b * 1e1, color=color.blue)

            print()
