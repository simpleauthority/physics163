from vpython import *

# wire size constants
y_min = -10  # bottom end from origin, meters
y_max = 10  # top end from origin, meters
num_slices = 600  # how many slices to cut wire into
wire_length = y_max - y_min  # length of wire, meters
dy = wire_length / num_slices  # length of each slice, meters

# computation constants
mu_naught = (4 * pi) * 1e-7  # tesla*meter/sec
i = 1.00  # amps
i_flow_direction = 1 if i > 0 else -1
integration_constant = (mu_naught * i) / (4 * pi)  # constant out front of BS law integral
point_of_interest = vec(5, 0, 0)  # point at which to calculate B field

# data holders
B_experimental = vec(0, 0, 0)  # total experimental magnetic field

distance_from_wire = sqrt(pow(point_of_interest.x, 2) + pow(point_of_interest.z, 2))  # distance from wire; also "a"
B_theory = 0  # total exact magnetic field
if distance_from_wire == 0:
    print("Failed to calculate B_theory. Distance from wire = 0!")
else:
    B_theory = (mu_naught * i) / (2 * pi * distance_from_wire)


# display constants
sat_level = 1e-7


# scales a target vector proportional to a quarter of the wire_length
def scale_factor(target):
    return (wire_length / 4) / mag(target)


# draw wire segments
wire = []
for y in arange(y_min, y_max, dy):
    segment = cylinder(pos=vec(0, y, 0), axis=vec(0, dy, 0), opacity=0.5)  # create segment on screen
    wire.append(segment)  # store for later

# draw current (for visual only)
for segment in wire:
    segment.i_arrow = arrow(pos=segment.pos + vec(0, dy / 4, 0), axis=vec(0, i * i_flow_direction * 0.75, 0), color=color.red)

# calculate magnetic field
for segment in wire:
    adjusted_source = segment.pos - vec(0, dy / 2, 0)  # middle of source/segment
    r = point_of_interest - adjusted_source  # calculate r vector from adjusted source to POI
    r_mag = mag(r)  # magnitude of r vector
    ds = segment.axis  # differential length of wire

    if mag(r) == 0:
        print(f"r = 0 for source {adjusted_source}; B_field would be infinite at this area. Skipping iteration.")
        continue

    segment.dB = integration_constant * (cross(ds, r) / pow(r_mag, 3))  # differential B field
    B_experimental += segment.dB  # add diff B to total B

# desaturate B_experimental if necessary
desaturated_b_experimental = B_experimental
if mag(desaturated_b_experimental) > sat_level:
    print("B_experimental size greater than defined saturation cap. The value will be desaturated.")
    desaturated_b_experimental = sat_level * hat(B_experimental)

# draw B total arrow
B_total_arrow = arrow(pos=point_of_interest, axis=2 * hat(B_experimental), color=color.red if mag(B_experimental) > mag(desaturated_b_experimental) else color.white, opacity=mag(B_experimental) / mag(desaturated_b_experimental))

# print results
print(f"L={wire_length}m, N={num_slices} segments, ds={dy}m")
print(f"B_experimental = {B_experimental} = {mag(B_experimental)}")
print(f"B_theory = {B_theory}")

if B_theory == 0:
    print("B_theory = 0, cannot calculate percent difference!")
else:
    print(f"% diff from theory = {(((mag(B_experimental) - B_theory) / B_theory) * 100):.5f}%")
