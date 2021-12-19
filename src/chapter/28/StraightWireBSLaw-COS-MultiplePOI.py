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

# axes
line_x = cylinder(pos=vec(-12, 0, 0), axis=vec(24, 0, 0), radius=0.1, color=color.white)
line_y = cylinder(pos=vec(0, y_min - 2, 0), axis=vec(0, 2 * (y_max + 2), 0), radius=0.1, color=color.white)

# draw wire
wire = []
for y in arange(y_min, y_max, dy):
    segment = cylinder(pos=vec(0, y, 0), axis=vec(0, dy, 0), opacity=0.5)  # create segment on screen
    segment.i_arrow = arrow(pos=segment.pos + vec(0, dy / 4, 0), axis=vec(0, i * 0.75, 0), color=color.red)  # draw current (for visual only)
    wire.append(segment)


# noinspection PyShadowingNames
def calc_mag_field(segments, point_of_interest):
    b_experimental = vec(0, 0, 0)

    r_tot = vec(0, 0, 0)
    ds_tot = vec(0, 0, 0)
    for segment in segments:
        segment_pos = segment.pos + vec(0, dy/2, 0)
        ds = segment.axis

        r = point_of_interest - segment_pos  # calculate r vector from middle of source to POI
        if mag(r) == 0:
            print(f"r = 0; B_field would be infinite at this area. Skipping iteration.")
            continue

        r_tot += r
        ds_tot += ds

        db = integration_constant * cross(ds, r) / (mag(r) ** 3)  # differential b
        b_experimental += db  # add diff B to total B

    return b_experimental, hat(cross(ds_tot, r_tot))


# draw POIs, calculate B at those POIs, and draw arrows
b_fields = []
for x in arange(-10, 10.2, 0.1):
    if x == 0:
        continue

    point_of_interest = vec(x, 0, 0)
    b, r_hat = calc_mag_field(wire, point_of_interest)
    b_mag = mag(b)

    desat_b = b
    if mag(desat_b) > sat_level:
        desat_b = sat_level * hat(b)

    desat_b_mag = mag(desat_b)
    if desat_b_mag != 0:
        b_arrow_color = color.red if b_mag > desat_b_mag else color.white
        b_arrow_opacity = b_mag / desat_b_mag
        b_arrow = arrow(pos=point_of_interest, axis=desat_b * 1e8, color=b_arrow_color, opacity=b_arrow_opacity)

    b_theory = vec(0, 0, 0)
    b_theory_mag = 0
    a = mag(point_of_interest)
    if a != 0:
        b_theory = (mu_naught * i) / (2 * pi * a) * r_hat
        b_theory_mag = mag(b_theory)

        desat_b_th = b_theory
        if mag(desat_b_th) > sat_level:
            desat_b_th = sat_level * hat(desat_b_th)

        desat_b_th_mag = mag(desat_b_th)
        if desat_b_th_mag != 0:
            b_th_arrow_color = color.yellow if b_theory_mag > desat_b_th_mag else color.blue
            b_th_arrow_opacity = b_theory_mag / desat_b_th_mag
            b_th_arrow = arrow(pos=point_of_interest, axis=desat_b_th * 1e8, color=b_th_arrow_color, opacity=b_th_arrow_opacity)

    b_fields.append((x, b_mag, b_theory_mag, ((b_mag - b_theory_mag) / b_theory_mag) * 100))

    # print(f"b @ {point_of_interest} = {b} (= {b_mag:.3e})")
    # print(f"b_exact @ {point_of_interest} = {b_theory} = ({b_theory_mag:.3e})")
    # print(f"pdiff @ {point_of_interest} = {((b_mag - b_theory_mag) / b_theory_mag) * 100:.2f}%")
    # print()

for field in b_fields:
    print(f"{field[0]},{field[1]},{field[2]},{field[3]}%")
