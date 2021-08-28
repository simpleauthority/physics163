from vpython import *

from physics.ElectricCharge import ElectricCharge
from physics.ElectricForce import ElectricForce

# Configure the scene
scene.width = 800
scene.height = 600
global_arrow_scale_factor = 1e12


class CoolTriangleProblem:
    def __init__(self):
        self.trace_log = False  # whether or not to log a bunch of crap
        self.dt = 1e-3  # how much to step the loop per iteration
        self.t = 0  # how much time has elapsed
        self.q = 1e-8  # e; magnitude of electron charge

        self.x_axis = cylinder(pos=vec(-6e-3, 0, 0), axis=vec(12e-3, 0, 0), radius=3e-5)
        self.y_axis = cylinder(pos=vec(0, -1e-3, 0), axis=vec(0, 10e-3, 0), radius=3e-5)

        # Create q1-q3, statically positioned charges positioned in a triangle shape
        self.charge1 = ElectricCharge(value=-1 * self.q, position=vec(0, 8e-4, 0), name="q1", value_alias="-q",
                                      draw=True,
                                      extra=dict(mass=1e-6), object_props=dict(radius=5e-5, color=color.red))

        self.charge2 = ElectricCharge(value=-1 * self.q, position=vec(-8e-4, 0, 0), name="q2", value_alias="-q",
                                      draw=True,
                                      extra=dict(mass=1e-6), object_props=dict(radius=5e-5, color=color.red))

        self.charge3 = ElectricCharge(value=-1 * self.q, position=vec(8e-4, 0, 0), name="q3", value_alias="-q",
                                      draw=True,
                                      extra=dict(mass=1e-6), object_props=dict(radius=5e-5, color=color.red))

        # Create q4, a dynamically positioned charge
        self.charge4 = ElectricCharge(value=self.q, position=vec(4e-4, 6e-4, 0), name="q4", value_alias="q", draw=True,
                                      extra=dict(mass=1e-7), object_props=dict(radius=3e-5, color=color.blue))
        self.charge4_a = vec(0, 0, 0)
        self.charge4_v = vec(0, 0, 0)

        # The camera should follow q4
        scene.camera.follow(self.charge4.object)

        # Create and draw force14, force24, force34
        self.force14 = ElectricForce(q1=self.charge1, q2=self.charge4, draw=True,
                                     base_scale_factor=global_arrow_scale_factor, trace_log=self.trace_log,
                                     indicator_props=dict(color=self.charge1.object_props['color'], opacity=0.5))

        self.force24 = ElectricForce(q1=self.charge2, q2=self.charge4, draw=True,
                                     base_scale_factor=global_arrow_scale_factor, trace_log=self.trace_log,
                                     indicator_props=dict(color=self.charge2.object_props['color'], opacity=0.5))

        self.force34 = ElectricForce(q1=self.charge3, q2=self.charge4, draw=True,
                                     base_scale_factor=global_arrow_scale_factor, trace_log=self.trace_log,
                                     indicator_props=dict(color=self.charge3.object_props['color'], opacity=0.5))

        # Calculate the initial net force magnitude
        self.net_force = self.force14.value + self.force24.value + self.force34.value
        self.net_force_mag = mag(self.net_force)

        # # Create and draw a graph plotting x in nanometers vs net force magnitude in piconewtons
        # self.t_net_force_graph = graph(width=800, height=225, xmin=-4, xmax=6, ymin=-6000, ymax=6000,
        #                                title="<b><i>x</i> (nm) vs <i>F<sub>net mag</sub></i> (pN)</b>",
        #                                xtitle="<i>x</i> (nm)", ytitle="<i>F<sub>net mag</sub></i> (pN)",
        #                                foreground=vec(0, 0, 0), background=vec(1, 1, 1))
        #
        # # Create a curve for plotting on the graph
        # self.t_net_force_curve = gcurve(color=vec(0, 0.4, 1))

    def start_sim(self):
        print("loop dt = ", self.dt)
        while self.t <= 1000:
            # This loop will run at a maximum of 90 its/sec
            rate(60)

            print("itr for t = ", self.t)

            # Tick the forces
            for force in (self.force14, self.force24, self.force34):
                force.tick()

            # Get net force
            self.net_force = self.force14.value + self.force24.value + self.force34.value
            self.net_force_mag = mag(self.net_force)
            print("net force, ", self.net_force)
            print("net force mag, ", self.net_force_mag)

            # Tick q4 accel
            q4_mass = self.charge4.extra['mass']
            q4_a = self.net_force / q4_mass
            print("q4 accel, ", self.charge4_a)
            self.charge4_a = q4_a

            # Tick q4 vel
            self.charge4_v += self.charge4_a * self.dt
            print("q4 vel, ", self.charge4_v)

            # Tick q4 pos
            q4_pos = self.charge4.position + (self.charge4_v * self.dt)
            print("q4 pos, ", q4_pos)

            self.charge4.tick_obj_pos(q4_pos)
            for force in (self.force14, self.force24, self.force34):
                force.set_q2_pos(q4_pos)

            # Add datapoint to the plot
            # self.t_net_force_curve.plot(self.t, self.net_force.y)

            # # Check if we've reached force equilibrium, allowing for small error margin
            # if 0 <= self.net_force_mag <= 1e-5:
            #     self.force14.scale_indicator(scale_factor=1)
            #     self.force24.scale_indicator(scale_factor=1)
            #     self.force24.scale_indicator(scale_factor=1)
            #
            #     print("Dynamic charge has reached force equilibrium. Arrow sizes have been adjusted larger.")
            #
            #     break

            self.t += self.dt
            print("\n")

            print("\n\n================\n\n")


# Start the simulation
sim = CoolTriangleProblem()
sim.start_sim()
