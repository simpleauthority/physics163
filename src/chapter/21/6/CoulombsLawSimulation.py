from vpython import *

from helper.Convert import Convert
from helper.Unit import Unit
from physics.ElectricCharge import ElectricCharge
from physics.ElectricForce import ElectricForce

# Configure the scene
scene.width = 800
scene.height = 600
global_arrow_scale_factor = 2


class CoulombsLawSimulation:
    # Simulation configuration settings
    paused = False  # whether or not the sim is paused
    logging = True  # whether or not we are logging messages (such as values of r13, r23, f13, f23, etc.)
    x_step = 0.5e-11  # how much to step the loop per iteration

    # Physical constants in use for the simulation
    D = Convert.to_base(1, original_unit=Unit.NANO)  # distance of each statically positioned charge from origin
    E = 1.602e-19  # e; magnitude of electron charge
    X_MIN = -4 * D  # x min position
    X_MAX = 6 * D  # x max position

    def __init__(self):
        """Sets up the scene for the simulation"""
        # Set simulation x at X_MIN
        self.x = self.X_MIN

        # Create coordinate axis for visual reference
        self.x_axis = cylinder(pos=vec(self.X_MIN, 0, 0), axis=vec(2*self.X_MAX, 0, 0),
                               radius=Convert.to_base(5, original_unit=Unit.PICO))

        # Create q1, a statically positioned charge located at D i-hat
        self.charge1 = ElectricCharge(value=-1 * self.E, pos=vec(self.D, 0, 0), name="q1", value_alias="-e", draw=True,
                                      object_props=dict(radius=0.08 * self.D, color=color.cyan))

        # Create q2, a statically positioned charge located at -D i-hat
        self.charge2 = ElectricCharge(value=2 * self.E, pos=vec(-self.D, 0, 0), name="q2", value_alias="2e", draw=True,
                                      object_props=dict(radius=0.12 * self.D, color=color.red))

        # Create q3, a dynamically positioned charge
        self.charge3 = ElectricCharge(value=-1 * self.E, pos=vec(self.x, 0, 0), name="q3", value_alias="-e", draw=True,
                                      object_props=dict(radius=0.03 * self.D, color=vec(0.8, 0, 1),
                                                        opacity=0.8))

        # The camera should follow q3
        scene.camera.follow(self.charge3.object)

        # Create and draw force13, the force of q1 on q3
        self.force13 = ElectricForce(q1=self.charge1, q2=self.charge3, draw=True,
                                     base_scale_factor=global_arrow_scale_factor, logging=self.logging,
                                     indicator_props=dict(color=self.charge1.object_props['color'], opacity=0.5))

        # Create and draw force23, the force of q2 on q3
        self.force23 = ElectricForce(q1=self.charge2, q2=self.charge3, draw=True,
                                     base_scale_factor=global_arrow_scale_factor, logging=self.logging,
                                     indicator_props=dict(color=self.charge2.object_props['color'], opacity=0.5))

        # Calculate the initial net force magnitude
        self.net_force_mag = mag(self.force13.value + self.force23.value)

        # Create and draw a graph plotting x in nanometers vs net force magnitude in piconewtons
        self.x_net_force_graph = graph(width=800, height=225, xmin=-4, xmax=6, ymin=0, ymax=6000,
                                       title="<b><i>x</i> (nm) vs <i>F<sub>net mag</sub></i> (pN)</b>",
                                       xtitle="<i>x</i> (nm)", ytitle="<i>F<sub>net mag</sub></i> (pN)",
                                       foreground=vec(0, 0, 0), background=vec(1, 1, 1))

        # Create a curve for plotting on the graph
        self.x_net_force_curve = gcurve(color=vec(0, 0.4, 1))

        # Create UI buttons
        self.toggle_logging_button = button(bind=self.toggle_logging, text="Toggle Logging")
        self.pause_button = button(bind=self.toggle_pause, text="Pause/Unpause Simulation")
        self.reset_sim_button = button(bind=self.reset_sim, text="Reset Simulation")

    def toggle_logging(self):
        logging = not self.logging

        for item in (self, self.force13, self.force23):
            item.logging = logging

        print("Logging has been {0}".format("enabled" if self.logging else "disabled"))  # we print this one regardless

    def toggle_pause(self):
        if self.paused:
            self.paused = False
            self.start_sim(start_x=self.x)
            if self.logging:
                print("Simulation unpaused.")
        else:
            self.paused = True
            if self.logging:
                print("Simulation paused.")

    def reset_sim(self):
        # if the sim is running, we need to pause it
        if not self.paused:
            self.toggle_pause()

        self.x = self.X_MIN

        if self.logging:
            print("Simulation reset.")

    def start_sim(self, start_x=X_MIN):
        x = start_x

        print("Simulation will begin at x = {0:.2e}m".format(x)) if self.logging else None

        while True:
            # This loop will run at a maximum of 60 its/sec
            rate(60)

            print("INFO: Starting iteration for x = {0:.2e}m".format(x)) if self.logging else None

            # Tick q3's new position
            q3_pos = vec(x, 0, 0)
            self.charge3.tick_obj_pos(q3_pos)
            self.force13.set_q2_pos(q3_pos)
            self.force23.set_q2_pos(q3_pos)

            # Tick the forces
            self.force13.tick()
            self.force23.tick()

            # Recalculate the net force
            self.net_force_mag = mag(self.force13.value + self.force23.value)

            # Add datapoint to the plot
            self.x_net_force_curve.plot(Convert.to_nano(x), Convert.to_pico(self.net_force_mag))

            # Check if we've reached force equilibrium, allowing for 1pm of error margin
            if 0 < self.net_force_mag * 1e9 <= 0.0001:
                self.force13.scale_indicator(scale_factor=2e3)
                self.force23.scale_indicator(scale_factor=2e3)

                if self.logging:
                    print("Dynamic charge has reached force equilibrium. Arrow sizes have been adjusted larger.")

                break

            # break out of the loop if the user paused us
            # we want to do this before incrementing x otherwise we lose one iteration
            if self.paused:
                print("Simulation has been paused at x = {0:.2e}".format(x))
                break

            x += self.x_step

        self.x = x


# Start the simulation
sim = CoulombsLawSimulation()
sim.start_sim()
