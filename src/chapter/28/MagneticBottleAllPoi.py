from vpython import *

# constants
# ring_radius = 0.105  # radius of ring, meters
ring_radius = 0.210
num_slices = 360  # how many slices to cut ring into
theta_min = 0  # min angle of ring, radians
theta_max = 2 * pi  # max angle of ring, radians
total_theta = theta_max - theta_min  # total angle of ring, radians
dtheta = total_theta / num_slices  # differential angle of each slice, radians
mu_naught = (4 * pi) * 1e-7  # tesla*meter/sec

sat_level = 1  # max size of arrow

# size constants
x_min = z_min = -1.25
y_min = -0.75
x_max = z_max = 2.50
y_max = 1.50

# axes
line_x = cylinder(pos=vec(x_min, 0, 0), axis=vec(x_max, 0, 0), radius=0.0025)
line_y = cylinder(pos=vec(0, y_min, 0), axis=vec(0, y_max, 0), radius=0.0025)
line_z = cylinder(pos=vec(0, 0, z_min), axis=vec(0, 0, z_max), radius=0.0025)
label_x = label(pos=line_x.pos + line_x.axis, text='x', height=10)  # set axes labels
label_y = label(pos=line_y.pos + line_y.axis, text='y', height=10)
label_z = label(pos=line_z.pos + line_z.axis, text='z', height=10)

# set up camera
scene.camera.rotate(radians(-15), vec(1, 0, 0))
scene.camera.rotate(radians(15), vec(0, 1, 0))
scene.camera.pos += vec(0.45, 0.30, -0.6)
scene.autoscale = False


# get integration constant
def integration_constant(current):
    return (mu_naught * current) / (4 * pi)  # constant out front of BS law integral


# get direction of any theta position on the ring
def calc_theta_hat(theta):
    return vec(0, cos(theta), -sin(theta))  # yz plane, x set to zero


# get differential arclength of ring
def calc_ds(theta):
    return ring_radius * dtheta * calc_theta_hat(theta)


# calculate the magnetic field of the ring at a specific position
def calc_mag_field(ring, poi, current):
    B_total = vec(0, 0, 0)  # total magnetic field

    for theta in arange(theta_min, theta_max, dtheta):
        segment = ring_radius * vec(ring.pos.x, ring.pos.y + sin(theta), ring.pos.z + cos(theta))
        r = poi - segment  # r vector from segment to arbitrary POI --ring in yz plane--
        r_mag = mag(r)  # mag of r vector

        ds = calc_ds(theta)  # differential arclength of a specific theta

        if r_mag != 0:
            B_total += integration_constant(current) * (cross(ds, r) / r_mag ** 3)  # append differential B to total B

    return B_total


def scale_factor(b):
    factor = ring_radius / mag(b)
    # print("Scale factor will be ", factor)
    return factor


# draw left ring
left_ring = ring(pos=vec(-1, 0, 0), axis=vec(1, 0, 0), radius=ring_radius, thickness=0.005)
left_current = -300  # amps

# # draw left poi
# left_poi = left_ring.pos
# left_poi_indicator = sphere(pos=left_poi, radius=0.025, color=color.red)
# left_exp_b = calc_mag_field(left_ring, left_poi, left_current)  # mag field at POI
# left_exp_b_arrow = arrow(pos=left_poi, axis=left_exp_b * 5e4, color=color.blue)
# print(mag(left_exp_b))

# draw right ring
right_ring = ring(pos=vec(1, 0, 0), axis=vec(1, 0, 0), radius=ring_radius, thickness=0.005)
right_current = 300  # amps

# # draw right poi
# right_poi = right_ring.pos
# right_poi_indicator = sphere(pos=right_poi, radius=0.025, color=color.red)
# right_exp_b = calc_mag_field(right_ring, right_poi, right_current)  # mag field at POI
# right_exp_b_arrow = arrow(pos=right_poi, axis=right_exp_b * 5e4, color=color.blue)
# print(mag(right_exp_b))

# draw pois and calc data for every point in space
dx = dy = dz = 0.25

smallest_b = 30
largest_b = 0

for x in arange(x_min, x_max + dx, dx):
    for y in arange(y_min, y_max + dy, dy):
        for z in arange(z_min, z_max + dz, dz):
            poi = vec(x, y, z)

            exp_b = calc_mag_field(left_ring, poi, left_current) + calc_mag_field(right_ring, poi, right_current)
            # print(f"exp b at ({x}, {y}, {z}): {mag(exp_b)}")

            exp_b_mag = mag(exp_b)

            if exp_b_mag > largest_b:
                largest_b = exp_b_mag
            elif exp_b_mag < smallest_b:
                smallest_b = exp_b_mag

            if exp_b_mag > sat_level:
                exp_b = sat_level * hat(exp_b)
                exp_b_mag = mag(exp_b)

            b_arrow = arrow(pos=poi, axis=exp_b * scale_factor(exp_b), color=color.blue)

print("smallest b seen", smallest_b)
print("largest b seen", largest_b)