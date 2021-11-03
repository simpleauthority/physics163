from vpython import *

# constants
ring_radius = 5  # radius of ring, meters
num_slices = 36  # how many slices to cut ring into; num slices 360 causes huge pdiff why?
theta_min = 0  # min angle of ring, radians
theta_max = 2 * pi  # max angle of ring, radians
total_theta = theta_max - theta_min  # total angle of ring, radians
dtheta = total_theta / num_slices  # differential angle of each slice, radians

mu_naught = (4 * pi) * 1e-7  # tesla*meter/sec
current = -300.0  # amps
integration_constant = (mu_naught * current) / (4 * pi)  # constant out front of BS law integral

scale_factor = 2e-14  # factor by which to scale arrows

# axes
line_x = cylinder(pos=vec(-5, 0, 0), axis=vec(10, 0, 0), radius=0.05)
line_y = cylinder(pos=vec(0, -5, 0), axis=vec(0, 10, 0), radius=0.05)
line_z = cylinder(pos=vec(0, 0, -5), axis=vec(0, 0, 10), radius=0.05)
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

# draw poi and calc data
point_of_interest = vec(4, 0, 0)
point_of_interest_indicator = sphere(pos=point_of_interest, radius=0.15, color=color.red)

# calculate exp b field
exp_b_field = calc_mag_field(point_of_interest)  # mag field at POI
exp_b_field_arrow = arrow(pos=point_of_interest, axis=exp_b_field * 1e5, color=color.blue)  # arrow for exp_b_field
print(f"exp b field = {exp_b_field}")
print(f"hat exp b field = {hat(exp_b_field)}")
print(f"magnitude exp b field = {mag(exp_b_field)}")

# find theoretical b field
th_b_field = abs((mu_naught * current * ring_radius ** 2) / (2 * (ring_radius ** 2 + point_of_interest.x ** 2) ** 1.5))
# th_b_field = (mu_naught * current) / (2*ring_radius)
print(f"magnitude th b field = {th_b_field}")

# find pdiff from theory
pdiff = ((mag(exp_b_field) - th_b_field) / th_b_field) * 100   # percent difference calc, ((exp - theo)/theo) * 100
print(f"% diff from theory = {pdiff}%")
