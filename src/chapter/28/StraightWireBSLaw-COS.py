from vpython import *

# wire size constants
num_slices = 200  # how many slices to cut wire into
wire_length = 20  # length of wire, meters
y_min = -(wire_length / 2)  # bottom end from origin, meters
y_max = wire_length / 2  # top end from origin, meters
dy = wire_length / num_slices  # length of each slice, meters
print(f"dy = {dy}")

# computation constants
mu_naught = (4 * pi) * 1e-7  # tesla*meter/sec
i = 1.00  # amps
i_flow_direction = 1 if i > 0 else -1
integration_constant = (mu_naught * i) / (4 * pi)  # constant out front of BS law integral
point_of_interest = vec(1, 0, 0)  # point at which to calculate B field

# data holders
B_experimental = vec(0, 0, 0)  # total experimental magnetic field

# display constants
sat_level = 1e-7


# scales a target vector proportional to a quarter of the wire_length
def scale_factor(target):
    return (wire_length / 4) / mag(target)


# axes
line_x = cylinder(pos=vec(-5, 0, 0), axis=vec(10, 0, 0), radius=0.1, color=color.white)
line_y = cylinder(pos=vec(0, y_min - 2, 0), axis=vec(0, 2 * (y_max + 2), 0), radius=0.1, color=color.white)

# draw wire
wire = []
for y in arange(y_min, y_max, dy):
    segment = cylinder(pos=vec(0, y, 0), axis=vec(0, dy, 0), opacity=0.5)  # create segment on screen
    # segment.i_arrow = arrow(pos=segment.pos + vec(0, dy / 4, 0), axis=vec(0, i * 0.75, 0), color=color.red)  # draw current (for visual only)
    wire.append(segment)

# find b total
for segment in wire:
    r = point_of_interest - (segment.pos + vec(0, dy / 2, 0))  # calculate r vector from middle of source to POI
    if mag(r) == 0:
        print(f"r = 0; B_field would be infinite at this area. Skipping iteration.")
        continue

    ds = segment.axis  # length of wire segment
    db = integration_constant * cross(ds, r) / (mag(r) ** 3)  # differential b
    B_experimental += db  # add diff B to total B

# desaturate B_experimental if necessary
desaturated_b_experimental = B_experimental
if mag(desaturated_b_experimental) > sat_level:
    print("B_experimental size greater than defined saturation cap. The value will be desaturated.")
    desaturated_b_experimental = sat_level * hat(B_experimental)

# draw B total arrow
if mag(desaturated_b_experimental) == 0:
    print("B_experimental = 0, no arrow to draw!")
else:
    B_total_arrow = arrow(pos=point_of_interest,
                          axis=desaturated_b_experimental * scale_factor(desaturated_b_experimental),
                          color=color.red if mag(B_experimental) > mag(desaturated_b_experimental) else color.white,
                          opacity=mag(B_experimental) / mag(desaturated_b_experimental))

# calculate B_theory
B_theory = 0  # total exact magnetic field
a = mag(point_of_interest)
if a == 0:
    print("Failed to calculate B_theory. Distance from wire = 0!")
else:
    B_theory = (mu_naught * i) / (2 * pi * a)

# print results
print(f"L={wire_length}m (min={y_min}m, max={y_max}m), N={num_slices} segments")
print(f"B_experimental = {B_experimental} = {mag(B_experimental)}")
print(f"B_theory = {B_theory}")

if B_theory == 0:
    print("B_theory = 0, cannot calculate percent difference!")
else:
    print(f"% diff from theory = {(((mag(B_experimental) - B_theory) / B_theory) * 100):.5f}%")
