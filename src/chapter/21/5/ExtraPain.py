from vpython import *

# Configure the scene
scene.width = 800
scene.height = 600
scene.title = "<h2>Problem 21.5 On Steroids</h2><br /><strong>Close when done (this sim does not stop on its own).</strong><br /><br />"

# Constants
charge_radius = 3e-4
e = 1.602e-19
d = 6e-4
x = 7e-4


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
q1.m = 3e-4  # 0.0003 kg
q1.a = vec(0, 0, 0)
q1.v = vec(0, 0, 0)
q1.lab = label(pos=q1.pos, text="q1=e", height=11)

q2 = sphere(pos=vec(0, -d, 0), radius=5e-5, color=color.cyan)
q2.chg = e
q2.m = 3e-8  # 0.00000007 kg
q2.a = vec(0, 0, 0)
q2.v = vec(0, 0, 0)
q2.lab = label(pos=q2.pos, text="q2=e", height=11)

q3 = sphere(pos=vec(x, 0, 0), radius=5e-5, color=color.orange)
q3.chg = -e
q3.m = 3e-16  # 0.0000000000000003 kg
q3.a = vec(0, 0, 0)  # accel
q3.v = vec(0, 0, 0)  # velocity
q3.lab = label(pos=q3.pos, text="q3=-e", height=11)

# create forces & arrows
f12 = calc_force12(q1, q2)
f12arrow = arrow(pos=q2.pos, axis=f12 * scale_factor(f12), color=q1.color + q2.color, opacity=0.3)
f12arrow.lab = label(pos=f12arrow.pos + f12arrow.axis, text="f12", height=11)
# print("f12 = ", f12)

f13 = calc_force12(q1, q3)
f13arrow = arrow(pos=q3.pos, axis=f13 * scale_factor(f13), color=q1.color + q3.color, opacity=0.3)
f13arrow.lab = label(pos=f13arrow.pos + f13arrow.axis, text="f13", height=11)
# print("f13 = ", f13)

f21 = calc_force12(q2, q1)
f21arrow = arrow(pos=q1.pos, axis=f21 * scale_factor(f21), color=q2.color + q1.color, opacity=0.3)
f21arrow.lab = label(pos=f21arrow.pos + f21arrow.axis, text="f21", height=11)
# print("f21 = ", f21)

f23 = calc_force12(q2, q3)
f23arrow = arrow(pos=q3.pos, axis=f23 * scale_factor(f23), color=q2.color + q3.color, opacity=0.3)
f23arrow.lab = label(pos=f23arrow.pos + f23arrow.axis, text="f23", height=11)
# print("f23 = ", f23)

f31 = calc_force12(q3, q1)
f31arrow = arrow(pos=q1.pos, axis=f31 * scale_factor(f31), color=q3.color + q1.color, opacity=0.3)
f31arrow.lab = label(pos=f31arrow.pos + f31arrow.axis, text="f31", height=11)
# print("f21 = ", f21)

f32 = calc_force12(q3, q2)
f32arrow = arrow(pos=q2.pos, axis=f32 * scale_factor(f32), color=q3.color + q2.color, opacity=0.3)
f32arrow.lab = label(pos=f32arrow.pos + f32arrow.axis, text="f32", height=11)
# print("f23 = ", f23)

# get net forces
fnet1 = f21 + f31
fnet1arrow = arrow(pos=q1.pos, axis=fnet1 * scale_factor(fnet1), color=color.yellow, opacity=0.3)
fnet1arrow.lab = label(pos=fnet1arrow.pos + fnet1arrow.axis, text="f_net1", height=11)
# print("fnet1 = ", fnet1)

fnet2 = f12 + f32
fnet2arrow = arrow(pos=q2.pos, axis=fnet2 * scale_factor(fnet2), color=color.yellow, opacity=0.3)
fnet2arrow.lab = label(pos=fnet2arrow.pos + fnet2arrow.axis, text="f_net2", height=11)
# print("fnet2 = ", fnet2)

fnet3 = f13 + f23
fnet3arrow = arrow(pos=q3.pos, axis=fnet3 * scale_factor(fnet3), color=color.yellow, opacity=0.3)
fnet3arrow.lab = label(pos=fnet3arrow.pos + fnet3arrow.axis, text="f_net3", height=11)
# print("fnet3 = ", fnet3)

# Now that everything is drawn, no more autoscaling
scene.autoscale = False

# Sim vars
t = 0
dt = 0.01
sim_speed = 6

# Go until user stops it
while True:
    rate(sim_speed / dt)

    # print("Starting iteration for t = ", t)

    # update forces & arrows
    f12 = calc_force12(q1, q2)
    # print("f13 = ", f12)
    f12arrow.pos = q2.pos
    f12arrow.axis = f12 * scale_factor(f12)
    f12arrow.lab.pos = f12arrow.pos + f12arrow.axis

    f13 = calc_force12(q1, q3)
    # print("f13 = ", f13)
    f13arrow.pos = q3.pos
    f13arrow.axis = f13 * scale_factor(f13)
    f13arrow.lab.pos = f13arrow.pos + f13arrow.axis

    f21 = calc_force12(q2, q1)
    # print("f21 = ", f21)
    f21arrow.pos = q1.pos
    f21arrow.axis = f21 * scale_factor(f21)
    f21arrow.lab.pos = f21arrow.pos + f21arrow.axis

    f23 = calc_force12(q2, q3)
    # print("f23 = ", f23)
    f23arrow.pos = q3.pos
    f23arrow.axis = f23 * scale_factor(f23)
    f23arrow.lab.pos = f23arrow.pos + f23arrow.axis

    f31 = calc_force12(q3, q1)
    # print("f31 = ", f31)
    f31arrow.pos = q1.pos
    f31arrow.axis = f31 * scale_factor(f31)
    f31arrow.lab.pos = f31arrow.pos + f31arrow.axis

    f32 = calc_force12(q3, q2)
    # print("f32 = ", f32)
    f32arrow.pos = q2.pos
    f32arrow.axis = f32 * scale_factor(f32)
    f32arrow.lab.pos = f32arrow.pos + f32arrow.axis

    # update net forces
    fnet1 = f21 + f31
    # print("fnet1 = ", fnet1)
    fnet2 = f12 + f32
    # print("fnet2 = ", fnet2)
    fnet3 = f13 + f23
    # print("fnet3 = ", fnet3)

    fnet1arrow.pos = q1.pos
    fnet1arrow.axis = fnet1 * scale_factor(fnet1)
    fnet1arrow.lab.pos = fnet1arrow.pos + fnet1arrow.axis

    fnet2arrow.pos = q2.pos
    fnet2arrow.axis = fnet2 * scale_factor(fnet2)
    fnet2arrow.lab.pos = fnet2arrow.pos + fnet2arrow.axis

    fnet3arrow.pos = q3.pos
    fnet3arrow.axis = fnet3 * scale_factor(fnet3)
    fnet3arrow.lab.pos = fnet3arrow.pos + fnet3arrow.axis

    # update accel
    q1.a = fnet1 / q1.m
    # print("q1.a = ", q1.a)
    q2.a = fnet1 / q2.m
    # print("q2.a = ", q2.a)
    q3.a = fnet3 / q3.m
    # print("q3.a = ", q3.a)

    # update vel
    q1.v += q1.a * dt
    # print("q1.v = ", q1.v)
    q2.v += q2.a * dt
    # print("q2.v = ", q2.v)
    q3.v += q3.a * dt
    # print("q3.v = ", q3.v)

    # update pos
    q1.pos += q1.v * dt
    # print("q1.pos = ", q1.pos)
    q2.pos += q2.v * dt
    # print("q2.pos = ", q2.pos)
    q3.pos += q3.v * dt
    # print("q3.pos = ", q3.pos)

    # update labels
    q1.lab.pos = q1.pos
    q2.lab.pos = q2.pos
    q3.lab.pos = q3.pos

    t += dt
