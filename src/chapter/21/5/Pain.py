from vpython import *

# Configure the scene
scene.width = 800
scene.height = 600
scene.title = "<h2>Problem 21.5</h2><br /><strong>Close when done (this sim does not stop on its own).</strong><br /><br />"

# Constants
charge_radius = 3e-4
e = 1.602e-19
d = 3e-4
x = 5e-4


def calc_force12(first, second):
    k = 8.99e9
    r12 = second.pos - first.pos
    return (k * first.chg * second.chg * r12) / pow(mag(r12), 3)


def scale_factor(force):
    factor = charge_radius / mag(force)
    # print("Scale factor will be ", factor)
    return factor


# # axes
# cylinder(pos=vec(-8e-4, 0, 0), axis=vec(16e-4, 0, 0), radius=3e-6)
# cylinder(pos=vec(0, -3e-4, 0), axis=vec(0, 10e-4, 0), radius=3e-6)

# create charges
q1 = sphere(pos=vec(0, d, 0), radius=5e-5, color=color.red)
q1.chg = e
q1.lab = label(pos=q1.pos, text="q1=e", height=11)

q2 = sphere(pos=vec(0, -d, 0), radius=5e-5, color=color.cyan)
q2.chg = e
q2.lab = label(pos=q2.pos, text="q2=e", height=11)

q3 = sphere(pos=vec(x, 0, 0), radius=5e-5, color=color.orange)
q3.chg = -e
q3.m = 3e-16
q3.a = vec(0, 0, 0)  # accel
q3.v = vec(0, 0, 0)  # velocity
q3.lab = label(pos=q3.pos, text="q3=-e", height=11)

# create forces & arrows
# noinspection PyTypeChecker
f13 = calc_force12(q1, q3)
f13arrow = arrow(pos=q3.pos, axis=f13 * scale_factor(f13), color=q1.color + q3.color, opacity=0.3)
f13arrow.lab = label(pos=f13arrow.pos + f13arrow.axis, text="f13", height=11)
# print("f13 = ", f13)

# noinspection PyTypeChecker
f23 = calc_force12(q2, q3)
f23arrow = arrow(pos=q3.pos, axis=f23 * scale_factor(f23), color=q2.color + q3.color, opacity=0.3)
f23arrow.lab = label(pos=f23arrow.pos + f23arrow.axis, text="f23", height=11)
# print("f23 = ", f23)

# get net force
fnet = f13 + f23
fnetarrow = arrow(pos=q3.pos, axis=fnet * scale_factor(fnet), color=color.yellow, opacity=0.3)
fnetarrow.lab = label(pos=fnetarrow.pos + fnetarrow.axis, text="f_net", height=11)
# print("fnet = ", fnet)

# # Now that everything is drawn, no more autoscaling
# scene.autoscale = False

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
    f13 = calc_force12(q1, q3)
    # print("f13 = ", f14)
    f13arrow.pos = q3.pos
    f13arrow.axis = f13 * scale_factor(f13)
    f13arrow.lab.pos = f13arrow.pos + f13arrow.axis

    # noinspection PyTypeChecker
    f23 = calc_force12(q2, q3)
    # print("f23 = ", f24)
    f23arrow.pos = q3.pos
    f23arrow.axis = f23 * scale_factor(f23)
    f23arrow.lab.pos = f23arrow.pos + f23arrow.axis

    # update net force
    fnet = f13 + f23
    # print("fnet = ", fnet)
    fnetarrow.pos = q3.pos
    fnetarrow.axis = fnet * scale_factor(fnet)
    fnetarrow.lab.pos = fnetarrow.pos + fnetarrow.axis

    # update accel
    q3.a = fnet / q3.m
    # print("q3.a = ", q3.a)

    # update vel
    q3.v += q3.a * dt
    # print("q3.v = ", q3.v)

    # update pos
    q3.pos += q3.v * dt
    # print("q3.pos = ", q3.pos)

    # update q3's label
    q3.lab.pos = q3.pos

    t += dt
