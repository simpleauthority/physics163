from vpython import *

# wire size constants
num_slices = 200  # how many slices to cut wire into
wire_length = 20  # length of wire, meters
y_min = -(wire_length / 2)  # bottom end from origin, meters
y_max = wire_length / 2  # top end from origin, meters
dy = wire_length / num_slices  # length of each slice, meters
print(f"dy = {dy}\n")

# computation constants
mu_naught = (4 * pi) * 1e-7  # tesla*meter/sec
i = 1.00  # amps
i_flow_direction = 1 if i > 0 else -1
integration_constant = (mu_naught * i) / (4 * pi)  # constant out front of BS law integral

# display constants
sat_level = 1e-7


# scales a target vector proportional to a quarter of the wire_length
def scale_factor(target):
    return (wire_length / 4) / mag(target)


# axes
line_x = cylinder(pos=vec(-12, 0, 0), axis=vec(24, 0, 0), radius=0.1, color=color.white)
line_y = cylinder(pos=vec(0, y_min - 2, 0), axis=vec(0, 2 * (y_max + 2), 0), radius=0.1, color=color.white)

# draw wire
wire = []
for y in arange(y_min, y_max, dy):
    segment = cylinder(pos=vec(0, y, 0), axis=vec(0, dy, 0), opacity=0.5)  # create segment on screen
    segment.i_arrow = arrow(pos=segment.pos + vec(0, dy / 4, 0), axis=vec(0, i * 0.75, 0), color=color.red)  # draw current (for visual only)
    wire.append(segment)


def calc_mag_field(segments=[], points_of_interest=[]):
    b_experimental = vec(0, 0, 0)

    for segment in segments:
        segment_pos = segment.pos + vec(0, dy/2, 0)
        ds = segment.axis

        for point_of_interest in points_of_interest:
            r = point_of_interest - segment_pos  # calculate r vector from middle of source to POI
            if mag(r) == 0:
                print(f"r = 0; B_field would be infinite at this area. Skipping iteration.")
                continue

            db = integration_constant * cross(ds, r) / (mag(r) ** 3)  # differential b
            b_experimental += db  # add diff B to total B

    return b_experimental


# draw POIs, calculate B at those POIs, and draw arrows
for x in arange(-10, 12, 2):
    for y in arange(-10, 12, 2):
        if x == 0 and y == 0:
            continue

        point_of_interest = vec(x, y, 0)
        b = calc_mag_field(wire, [point_of_interest])
        b_mag = mag(b)

        desat_b = b
        if mag(desat_b) > sat_level:
            desat_b = sat_level * hat(b)

        desat_b_mag = mag(desat_b)
        if desat_b_mag != 0:
            b_arrow_color = color.red if b_mag > desat_b_mag else color.white
            b_arrow_opacity = b_mag / desat_b_mag
            b_arrow = arrow(pos=point_of_interest, axis=desat_b * scale_factor(desat_b), color=b_arrow_color, opacity=b_arrow_opacity)

        b_theory = 0
        a = mag(point_of_interest)
        if a != 0:
            b_theory = (mu_naught * i) / (2 * pi * a)

        print(f"b @ {point_of_interest} = {b} (= {b_mag:.3e})")
        print(f"b_exact @ {point_of_interest} = {b_theory:.3e}")
        print(f"pdiff @ {point_of_interest} = {((b_mag - b_theory) / b_theory) * 100:.2f}%")
        print()
