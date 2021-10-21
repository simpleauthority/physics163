from vpython import *

# constants
x_min = -10  # left end from origin, meters
x_max = 10  # right end from origin, meters
num_slices = 20  # how many slices to cut wire into
wire_length = x_max - x_min  # length of wire, meters
dx = wire_length / num_slices  # length of each slice, meters

mu_naught = (4 * pi) * 1e-7  # tesla*meter/sec
i = 1.00  # amps
i_flow_direction = 1 if i > 0 else -1
integration_constant = (mu_naught * i) / (4 * pi)  # constant out front of BS law integral
point_of_interest = vec(0, -3, 0)  # point at which to calculate B field
B_total = vec(0, 0, 0)  # total magnetic field

scale_factor = 1e8  # factor by which to scale arrows


# draw wire segments
wire = []
for x in arange(x_min, x_max, dx):
    segment = cylinder(pos=vec(x, 0, 0), axis=vec(dx, 0, 0), opacity=0.5)  # create segment on screen
    wire.append(segment)  # store for later

# draw current (for visual only)
for segment in wire:
    segment.i_arrow = arrow(pos=segment.pos + vec(dx / 4, 0, 0), axis=vec(i * i_flow_direction * 0.75, 0, 0), color=color.red)

# calculate magnetic field
for segment in wire:
    r = point_of_interest - (segment.pos + vec(dx / 2, 0, 0))  # calculate r vector from middle of source to POI
    r_mag = mag(r)  # magnitude of r vector
    ds = segment.axis  # differential length of wire

    segment.dB = integration_constant * (cross(ds, r) / pow(r_mag, 3))  # differential B field
    B_total += segment.dB  # add diff B to total B

# draw B total arrow
B_total_arrow = arrow(pos=point_of_interest, axis=B_total * scale_factor, color=color.blue)

print(B_total)
print((mu_naught * i)/(2*pi*point_of_interest.y))
