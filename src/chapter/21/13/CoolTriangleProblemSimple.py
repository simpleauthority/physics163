from vpython import *

# Configure the scene
scene.width = 800
scene.height = 600
scene.title = "<h2>Problem 21.13</h2><strong>Click to reposition moving charge.</strong><br /><strong>Close when done (this sim does not stop on its own).</strong><br /><br />"

# Constants
charge_radius = 3e-4
q = 1.602e-19


def calc_force12(first, second):
    k = 8.99e9
    r12 = second.pos - first.pos
    return (k * first.chg * second.chg * r12) / pow(mag(r12), 3)


def scale_factor(force):
    factor = charge_radius / mag(force)
    # print("Scale factor will be ", factor)
    return factor


# axes
cylinder(pos=vec(-8e-4, 0, 0), axis=vec(16e-4, 0, 0), radius=3e-6)
cylinder(pos=vec(0, -3e-4, 0), axis=vec(0, 10e-4, 0), radius=3e-6)

# create charges
q1 = sphere(pos=vec(0, 5e-4, 0), radius=5e-5, color=color.red)
q1.chg = -1 * q
q1.lab = label(pos=q1.pos, text="q1=-q", height=11)

q2 = sphere(pos=vec(-5e-4, 0, 0), radius=5e-5, color=color.cyan)
q2.chg = -1 * q
q2.lab = label(pos=q2.pos, text="q2=-q", height=11)

q3 = sphere(pos=vec(5e-4, 0, 0), radius=5e-5, color=color.green)
q3.chg = -1 * q
q3.lab = label(pos=q3.pos, text="q3=-q", height=11)

q4 = sphere(pos=vec(-8e-4, 7e-4, 0), radius=5e-5, color=color.orange)
q4.chg = q
q4.m = 3e-16
q4.a = vec(0, 0, 0)  # accel
q4.v = vec(0, 0, 0)  # velocity
q4.lab = label(pos=q4.pos, text="q4=q", height=11)

# Now that everything is drawn, no more autoscaling
scene.autoscale = False
scene.userzoom = False
scene.camera.pos += vec(0, 2e-4, 0)
scene.range = 8e-4

# create forces & arrows
# noinspection PyTypeChecker
f14 = calc_force12(q1, q4)
f14arrow = arrow(pos=q4.pos, axis=f14 * scale_factor(f14), color=q1.color + q4.color, opacity=0.3)
f14arrow.lab = label(pos=f14arrow.pos + f14arrow.axis, text="f14", height=11)
# print("f14 = ", f14)

# noinspection PyTypeChecker
f24 = calc_force12(q2, q4)
f24arrow = arrow(pos=q4.pos, axis=f24 * scale_factor(f24), color=q2.color + q4.color, opacity=0.3)
f24arrow.lab = label(pos=f24arrow.pos + f24arrow.axis, text="f24", height=11)
# print("f24 = ", f24)

# noinspection PyTypeChecker
f34 = calc_force12(q3, q4)
f34arrow = arrow(pos=q4.pos, axis=f34 * scale_factor(f34), color=q3.color + q4.color, opacity=0.3)
f34arrow.lab = label(pos=f34arrow.pos + f34arrow.axis, text="f34", height=11)
# print("f34 = ", f34)

# get net force
fnet = f14 + f24 + f34
fnetarrow = arrow(pos=q4.pos, axis=fnet * scale_factor(fnet), color=color.yellow, opacity=0.3)
fnetarrow.lab = label(pos=fnetarrow.pos + fnetarrow.axis, text="f_net", height=11)


# print("fnet = ", fnet)


# Move q4 to the mouse position and reset velocity on click
def move_q4_to_mouse(evt):
    q4.pos = evt.pos
    q4.v = vec(0, 0, 0)


scene.bind('click', move_q4_to_mouse)

# Sim vars
t = 0
dt = 0.01
sim_speed = 4

# Go until user stops it
while True:
    rate(sim_speed / dt)

    # print("Starting iteration for t = ", t)

    # update forces & arrows
    # noinspection PyTypeChecker
    f14 = calc_force12(q1, q4)
    # print("f14 = ", f14)
    f14arrow.pos = q4.pos
    f14arrow.axis = f14 * scale_factor(f14)
    f14arrow.lab.pos = f14arrow.pos + f14arrow.axis

    # noinspection PyTypeChecker
    f24 = calc_force12(q2, q4)
    # print("f24 = ", f24)
    f24arrow.pos = q4.pos
    f24arrow.axis = f24 * scale_factor(f24)
    f24arrow.lab.pos = f24arrow.pos + f24arrow.axis

    # noinspection PyTypeChecker
    f34 = calc_force12(q3, q4)
    # print("f34 = ", f34)
    f34arrow.pos = q4.pos
    f34arrow.axis = f34 * scale_factor(f34)
    f34arrow.lab.pos = f34arrow.pos + f34arrow.axis

    # update net force
    fnet = f14 + f24 + f34

    # checks if q4 is colliding with q1, q2, or q3
    # if it is, we remove that object from affecting net force
    # while not physically accurate, if the r-vec gets too small (approaches 0)
    # then the force approaches infinity and q4 flies off the screen entirely
    # so...this stops that
    for objects in ([q1, f14], [q2, f24], [q3, f34]):
        dist_squared = pow(objects[0].pos.x - q4.pos.x, 2) + pow(objects[0].pos.y - q4.pos.y, 2)
        if dist_squared <= pow(q1.radius + q2.radius, 2):
            fnet -= objects[1]

    # print("fnet = ", fnet)
    fnetarrow.pos = q4.pos
    fnetarrow.axis = fnet * scale_factor(fnet)
    fnetarrow.lab.pos = fnetarrow.pos + fnetarrow.axis

    # update accel
    q4.a = fnet / q4.m
    # print("q4.a = ", q4.a)

    # update vel
    q4.v += q4.a * dt
    # print("q4.v = ", q4.v)

    # update pos
    q4.pos += q4.v * dt
    # print("q4.pos = ", q4.pos)

    # update q4's label
    q4.lab.pos = q4.pos

    t += dt
