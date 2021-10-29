from vpython import *

# design
scene.title = "<h1>Magnetic Bottle Simulation</h1><br /><p>Watch as the particle gets stuck</p><br /><br />"
scene.width = 1024
scene.height = 768
scene.background = vec(161, 152, 151) / 255


# constants
ring_radius = 0.315  # radius of ring, meters
num_slices = 360  # how many slices to cut ring into
theta_min = 0  # min angle of ring, radians
theta_max = 2 * pi  # max angle of ring, radians
total_theta = theta_max - theta_min  # total angle of ring, radians
dtheta = total_theta / num_slices  # differential angle of each slice, radians
mu_naught = (4 * pi) * 1e-7  # tesla*meter/sec
current = -500  # amps
integration_constant = (mu_naught * current) / (4 * pi)  # constant out front of BS law integral

# size constants
x_min = z_min = -3
y_min = -0.75
x_max = z_max = 5
y_max = 2

# axes
line_x = cylinder(pos=vec(x_min, 0, 0), axis=vec(x_max, 0, 0), radius=0.0025, color=color.black)
line_y = cylinder(pos=vec(0, y_min, 0), axis=vec(0, y_max, 0), radius=0.0025, color=color.black)
line_z = cylinder(pos=vec(0, 0, z_min), axis=vec(0, 0, z_max), radius=0.0025, color=color.black)

# axis labels
label_x = label(pos=line_x.pos + line_x.axis, text='x', height=16, color=color.black)  # set axes labels
label_y = label(pos=line_y.pos + line_y.axis, text='y', height=16, color=color.black)
label_z = label(pos=line_z.pos + line_z.axis, text='z', height=16, color=color.black)

# set up camera
scene.camera.rotate(radians(-15), vec(1, 0, 0))
scene.camera.rotate(radians(15), vec(0, 1, 0))
scene.camera.pos += vec(0.45, 0.30, -0.6)
scene.autoscale = False


# get direction of any theta position on the ring
def calc_theta_hat(theta):
    return vec(0, cos(theta), -sin(theta))  # yz plane, x set to zero


# get differential arclength of ring
def calc_ds(theta):
    return ring_radius * dtheta * calc_theta_hat(theta)


# calculate the magnetic field of the ring at a specific position
def calc_mag_field(ring, poi):
    B_total = vec(0, 0, 0)  # total magnetic field

    for theta in arange(theta_min, theta_max, dtheta):
        segment = vec(ring.pos.x, ring.pos.y + ring_radius * sin(theta), ring.pos.z + ring_radius * cos(theta))
        r = poi - segment  # r vector from segment to arbitrary POI --ring in yz plane--
        r_mag = mag(r)  # mag of r vector

        ds = calc_ds(theta)  # differential arclength of a specific theta

        if r_mag != 0:
            B_total += integration_constant * ((cross(ds, r)) / r_mag ** 3)  # append differential B to total B

    return B_total


def scale_factor(b):
    factor = ring_radius / mag(b)
    # print("Scale factor will be ", factor)
    return factor


# draw left ring
left_ring = ring(pos=vec(x_min, 0, 0), axis=vec(1, 0, 0), radius=ring_radius, thickness=0.01, color=color.purple)

# draw right ring
right_ring = ring(pos=vec(x_min+x_max, 0, 0), axis=vec(1, 0, 0), radius=ring_radius, thickness=0.01, color=color.purple)

print(f"Magnetic field at origin: {calc_mag_field(left_ring, vec(0, 0, 0)) + calc_mag_field(right_ring, vec(0, 0, 0))}")

# draw pois and calc data for every point in space
dx = dy = dz = 0.35
B_min = B_max = 0
for x in arange(x_min + dx, (x_max / 2) - dx/2, dx):
    for y in arange(y_min / 3, y_max / 3, dy):
        for z in arange((z_min / 3) - dz, (z_max / 3), dz):
            poi = vec(x, y, z)
            exp_b = calc_mag_field(left_ring, poi) + calc_mag_field(right_ring, poi)

            b_arrow = arrow(pos=poi, axis=exp_b * scale_factor(exp_b), color=color.blue)

            exp_b_mag = mag(exp_b)
            if exp_b_mag > B_max:
                B_max = exp_b_mag
            elif exp_b_mag < B_min:
                B_min = exp_b_mag

            if exp_b_mag > 0:
                b_arrow.opacity = exp_b_mag / B_max
            elif exp_b_mag < 0:
                b_arrow.opacity = exp_b_mag / B_min

            b_arrow.opacity *= 0.7

# draw an electron in the b field
proton = sphere(pos=vec(0, ring_radius / 15, 0), radius=0.05, color=color.red)  # electron
proton.charge = 1.602e-19  # electron elementary charge
proton.mass = 1.672e-27  # mass of electron
proton.magnetic_field = calc_mag_field(left_ring, proton.pos) + calc_mag_field(right_ring, proton.pos)
proton.velocity = vec(0, 0, -((ring_radius * proton.charge * mag(proton.magnetic_field)) / (15 * proton.mass)))   # initial velocity of proton, moving in k-hat
proton.velocity.x=7*proton.velocity.z
# proton.velocity_arrow = arrow(pos=proton.pos, axis=proton.velocity * scale_factor(proton.velocity), color=color.purple)
proton.momentum = proton.mass * proton.velocity
proton.magnetic_force = cross(proton.charge * proton.velocity, proton.magnetic_field)
# proton.force_arrow = arrow(pos=proton.pos, axis=proton.magnetic_force * scale_factor(proton.magnetic_force), color=color.orange)

# animate the electron
t = 0
dt = (2 * pi * proton.pos.y) / (100 * proton.charge * mag(proton.velocity))

while True:
    # rate loop for testing
    rate(60)

    b_field = calc_mag_field(left_ring, proton.pos) + calc_mag_field(right_ring, proton.pos)
    print(f"Magnetic field is {b_field}T ({mag(b_field)}T)")

    # find force on electron due to B_total
    proton.magnetic_force = cross(proton.charge * proton.velocity, b_field)
    print(f"Force on electron is {proton.magnetic_force}N ({mag(proton.magnetic_force)}N)")

    # update electron's momentum
    proton.momentum += proton.magnetic_force * dt
    print(f"Momentum of electron is {proton.momentum}kgm/s")

    # update electron's velocity
    proton.velocity = proton.momentum / proton.mass
    print(f"Velocity of electron is {proton.velocity}m/s")

    # update the position due to the updated momentum
    proton.pos += (proton.momentum / proton.mass) * dt
    print(f"Position of electron is ({proton.pos.x:.2e}, {proton.pos.y:.2e}, {proton.pos.z:.2e})")

    # draw arrows
    # proton.velocity_arrow.pos = proton.pos
    # proton.velocity_arrow.axis = proton.velocity * 1e-3
    # proton.force_arrow.pos = proton.pos
    # proton.force_arrow.axis = proton.magnetic_force * 1e21

    print()
    t += dt
