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
line_x = cylinder(pos=vec(0.15, 0, 0), axis=vec(0.3, 0, 0), radius=0.0005)
line_y = cylinder(pos=vec(0, 0.15, 0), axis=vec(0, 0.3, 0), radius=0.0005)
line_z = cylinder(pos=vec(0, 0, 0.15), axis=vec(0, 0, 0.3), radius=0.0005)
label_x = label(pos=line_x.pos, text='x', height=10)  # set axes labels
label_y = label(pos=line_y.pos, text='y', height=10)
label_z = label(pos=line_z.pos, text='z', height=10)


# get differential arclength of ring
def calc_ds(theta):
    return ring_radius * dtheta * calc_theta_hat(theta)


# get direction of any theta position on the ring
def calc_theta_hat(theta):
    return vec(0, cos(theta), -sin(theta))  # yz plane, x set to zero


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

# # move camera
# scene.camera.pos += vec(0, 0, 0.2)  # move camera back a bit
# scene.autoscale = False  # do not move the camera automatically

# draw poi and calc data
point_of_interest = vec(0, 0, 0)
point_of_interest_indicator = sphere(pos=point_of_interest, radius=0.01, color=color.red)
label_point_of_interest_indicator = label(pos=point_of_interest_indicator.pos, text='POI', height=10)  # label for chosen POI

# calculate exp b field
exp_b_field = calc_mag_field(point_of_interest)  # mag field at POI
exp_b_field_arrow = arrow(pos=point_of_interest, axis=exp_b_field, color=color.blue)  # arrow for exp_b_field
print(f"exp b field = {exp_b_field}")
print(f"magnitude exp b field = {mag(exp_b_field):.3f}")

# find theoretical b field
# th_b_field = (mu_naught * current * ring_radius ** 2) / (2 * (ring_radius ** 2 + point_of_interest.x ** 2) ** 1.5)
th_b_field = (mu_naught * current) / (2*ring_radius)
print(f"th b field = {th_b_field:.3f}")

# find pdiff from theory
pdiff = ((mag(exp_b_field) - th_b_field) / th_b_field) * 100   # percent difference calc, ((exp - theo)/theo) * 100
print(f"% diff from theory = {pdiff:.3f}%")
