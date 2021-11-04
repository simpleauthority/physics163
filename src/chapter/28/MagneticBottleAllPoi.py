from vpython import *

# design
scene.title = "<h1>Magnetic Bottle Simulation</h1><p>Electron initially stuck in a magnetic bottle. The particle will corkscrew within the bottle until it hits a loss cone (not depicted) at which point<br />it will leave the system. Simulation does not stop on its own. Press \"Stop simulation\" or close the page when done.<br />"
scene.width = 960
scene.height = 720
scene.background = vec(161, 152, 151) / 255

# constants
ring_radius = 0.105  # radius of ring, meters
num_slices = 360  # how many slices to cut ring into
theta_min = 0  # min angle of ring, radians
theta_max = 2 * pi  # max angle of ring, radians
total_theta = theta_max - theta_min  # total angle of ring, radians
dtheta = total_theta / num_slices  # differential angle of each slice, radians
mu_naught = (4 * pi) * 1e-7  # tesla*meter/sec
current = -500  # amps
integration_constant = (mu_naught * current) / (4 * pi)  # constant out front of BS law integral

# size constants
x_min = -2
z_min = -1
y_min = -0.5
x_max = 4
z_max = 2
y_max = 1

# sim settings
run_sim = False

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
scene.camera.rotate(radians(18), vec(0, 1, 0))
scene.camera.pos += vec(0.6, 0.3, -1.25)
scene.autoscale = False


# essential methods
# calculate the magnetic field caused by the given rings at a given point of interest

# noinspection PyShadowingNames
def calc_mag_field(rings, point_of_interest):
    b_total = vec(0, 0, 0)

    for theta in arange(theta_min, theta_max, dtheta):
        theta_hat = vec(0, cos(theta), -sin(theta))
        ds = ring_radius * dtheta * theta_hat

        for ring in rings:
            segment = vec(ring.pos.x, ring.pos.y + ring_radius * sin(theta), ring.pos.z + ring_radius * cos(theta))
            r = point_of_interest - segment  # r vector from segment to arbitrary POI --ring in yz plane--
            r_mag = mag(r)  # mag of r vector

            if r_mag != 0:
                b_total += integration_constant * ((cross(ds, r)) / r_mag ** 3)  # append differential B to total B

    return b_total


# calculate a scale factor proportional to the ring_radius for a given vector
def scale_factor(b, prop_to=ring_radius):
    factor = prop_to / mag(b)
    # print("Scale factor will be ", factor)
    return factor


# draw a ring
def create_ring(pos):
    return ring(pos=pos, axis=vec(1, 0, 0), radius=ring_radius, thickness=0.01, color=color.purple)


# draw rings
left_ring = create_ring(vec(x_min, 0, 0))
right_ring = create_ring(vec(x_min+x_max, 0, 0))

# electron settings
electron_init = dict()
electron_init['pos'] = vec(0, ring_radius / 8, 0)
electron_init['charge'] = -1.602e-19
electron_init['mass'] = 9.10938356e-31
electron_init['b_field'] = calc_mag_field([left_ring, right_ring], electron_init['pos'])
electron_init['velocity'] = vec(0, 0, ((ring_radius * electron_init['charge'] * mag(electron_init['b_field'])) / (8 * electron_init['mass'])))
electron_init['velocity'].x = electron_init['velocity'].z
electron_init['momentum'] = electron_init['mass'] * electron_init['velocity']
electron_init['b_force'] = cross(electron_init['charge'] * electron_init['velocity'], electron_init['b_field'])


# draw the b field over points in space
def draw_b_field():
    arrow_sat = 0.15

    dx = dy = dz = 0.5

    x_start = x_min
    y_start = y_min
    z_start = z_min

    x_end = x_max + x_min
    y_end = y_max + y_min
    z_end = z_max + z_min

    for x in arange(x_min, x_max, dx):
        for y in arange(y_min, y_max, dy):
            for z in arange(z_min, z_max, dz):
                poi = vec(x, y, z)
                b_at_poi = calc_mag_field([left_ring, right_ring], poi)

                if x_start <= x <= x_end and y_start <= y <= y_end and z_start <= z <= z_end:
                    b_arrow = arrow(pos=poi, axis=b_at_poi * 1e6, color=color.blue, opacity=0.15)

                    if mag(b_arrow.axis) > arrow_sat:
                        b_arrow.axis = arrow_sat * hat(b_arrow.axis)

                    b_arrow.b = b_at_poi
                    b_arrow.poi = poi


# create physical electron from given settings
def set_electron(settings, already_exists=None):
    exists = already_exists is not None

    out = already_exists if exists else sphere(radius=0.025, color=color.red, make_trail=True, retain=150)
    out.pos = settings['pos']
    out.charge = settings['charge']
    out.mass = settings['mass']
    out.b_field = settings['b_field']
    out.velocity = settings['velocity']
    out.vperp2b = cross(out.velocity, out.b_field)
    out.momentum = settings['momentum']
    out.b_force = settings['b_force']

    label_pos = out.pos + vec(0, 0.15, 0)
    label_text = f"{mag(out.velocity) / 1000:.2f} km/s"

    if exists:
        out.velocity_label.pos = label_pos
        out.velocity_label.text = label_text
        out.velocity_arrow.pos = out.pos
        out.velocity_arrow.axis = out.velocity * scale_factor(out.velocity, prop_to=out.radius)
        out.force_arrow.pos = out.pos
        out.force_arrow.axis = out.b_force * scale_factor(out.b_force, prop_to=out.radius)
    else:
        out.velocity_label = label(pos=label_pos, text=label_text, height=10)
        out.velocity_arrow = arrow(pos=out.pos, axis=out.velocity * scale_factor(out.velocity), color=color.purple)
        out.force_arrow = arrow(pos=out.pos, axis=out.b_force * scale_factor(out.b_force), color=color.orange)

    return out


# draw electron
electron = set_electron(electron_init)

# draw b field
draw_b_field()
# print(f"Minimum B seen: {b_min}")
# print(f"Maximum B seen: {b_max}")


def reset_electron():
    global run_sim, electron_init, electron

    run_sim = False
    electron = set_electron(electron_init, electron)
    electron.clear_trail()


def simulate_electron():
    global run_sim, electron

    t = 0
    dt = 12e-8

    while True:
        # rate loop to 60 itr/sec
        rate(1024)

        # if the sim should not run, skip iteration
        if not run_sim:
            continue

        b_field = calc_mag_field([left_ring, right_ring], electron.pos)
        # print(f"Magnetic field is {b_field}T ({mag(b_field)}T)")

        # find force on electron due to B_total
        electron.magnetic_force = cross(electron.charge * electron.velocity, b_field)
        # print(f"Force on electron is {electron.magnetic_force}N ({mag(electron.magnetic_force)}N)")

        # update electron's momentum
        electron.momentum += electron.magnetic_force * dt
        # print(f"Momentum of electron is {electron.momentum}kgm/s")

        # update electron's velocity
        electron.velocity = electron.momentum / electron.mass
        electron.vperp2b = cross(electron.velocity, b_field)
        # print(f"Velocity of electron is {electron.velocity}m/s")

        # update the position due to the updated momentum
        electron.pos += electron.velocity * dt
        # print(f"Position of electron is ({electron.pos.x:.2e}, {electron.pos.y:.2e}, {electron.pos.z:.2e})")

        # update velocity label
        electron.velocity_label.text = f"{mag(electron.velocity) / 1000:.2f} km/s"
        electron.velocity_label.pos = electron.pos + vec(0, 0.15, 0)

        # update arrows
        electron.velocity_arrow.pos = electron.pos
        electron.velocity_arrow.axis = electron.velocity * scale_factor(electron.velocity)
        electron.force_arrow.pos = electron.pos
        electron.force_arrow.axis = electron.magnetic_force * scale_factor(electron.magnetic_force)

        # print()
        t += dt


def toggle_sim_running(b):
    global run_sim
    run_sim = not run_sim
    if run_sim:
        b.text = "Stop simulation"
    else:
        b.text = "Start simulation"


# def get_b_field_along_x():
#     b_fields = []
#     dx = (x_max - x_min) / 2000
#     for x in arange(x_min, x_min+x_max+dx, dx):
#         poi = vec(x, 0, 0)
#         b = mag(calc_mag_field([left_ring, right_ring], poi))
#         b_th = abs((mu_naught * current * pow(ring_radius, 2)) / (2 * pow(pow(ring_radius, 2) + pow(left_ring.pos.x - x, 2), 1.5))) + abs((mu_naught * current * pow(ring_radius, 2)) / (2 * pow(pow(ring_radius, 2) + pow(right_ring.pos.x - x, 2), 1.5)))
#         pdiff = ((b - b_th) / b_th) * 100
#         b_fields.append((x, b, b_th, pdiff))
#
#     for field in b_fields:
#         print(f"{field[0]}, {field[1]}, {field[2]}, {field[3]}%")


# GUI stuff
toggle_button = button(pos=scene.title_anchor, bind=toggle_sim_running, text="Start/stop simulation")
scene.append_to_title("  ")
reset_button = button(pos=scene.title_anchor, bind=reset_electron, text="Reset simulation")
scene.append_to_title("\n\n")

# get_b_field_along_x()

# start electron simulation
simulate_electron()
