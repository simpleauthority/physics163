# # draw a ball to act as a charge moving around ring
# print("debug: drawing ball")
# ball = sphere(pos=ring_radius * vec(0, cos(theta_min), sin(theta_min)), radius=0.01, color=color.red)  # ball
# print(ball.pos)

# ball.charge = -1.602e-19  # electron, coulombs
# ball.mass = 9.11e-31  # mass of electron, kilograms
# ball.momentum = vec(0, 0, 0)  # ball.momentum = ball.mass*ball.velocity
# ball.velocity = vec(0, 0.05, 0.05)

# animate ball
# magnetic_field = calc_mag_field(ball.pos)  # magnetic field
# magnetic_field_arrow = arrow(pos=ball.pos, axis=magnetic_field * scale_factor, color=color.blue)
#
# dt = 0.01  # how often to update ball
# sim_speed = 1  # sim speed for testing

# def scale_factor(magnetic_field):
#     factor = (ball.radius / mag(magnetic_field)) * 15
#     return factor
#
# # for later when POI is attached to ball.pos
# print("debug: animating ball")
# theta = theta_min
# while True:  # range equals (0,2pi,dtheta)
#     # rate the loop for testing
#     rate(sim_speed / dt)
#
#     # # follow euler-cromer method for moving the ball
#     # magnetic_field = calc_mag_field(ball.pos)
#     # force = cross(ball.charge * ball.velocity, magnetic_field)
#     # ball.momentum += force * dt
#     # ball.pos += (ball.momentum / ball.mass) * dt
#     # print(ball.pos)
#
#     # update the magnetic field arrow
#     # FOR LATER magnetic_field_arrow.axis = magnetic_field * scale_factor


# list_of_arrows.append(magnetic_field_arrow)


# test
# B_field_at_origin = calc_mag_field(vec(0, 0, 0))
# arrow = arrow(pos=vec(0, 0, 0), axis=B_field_at_origin * scale_factor, color=color.red)

# # calculate magnetic field
# for segment in ring:
#     r = point_of_interest - (segment.pos + vec(dx / 2, 0, 0))  # calculate r vector from middle of source to POI
#     r_mag = mag(r)  # magnitude of r vector
#     ds = segment.axis  # differential length of wire
#
#     segment.dB = integration_constant * (cross(ds, r) / pow(r_mag, 3))  # differential B field
#     B_total += segment.dB  # add diff B to total B