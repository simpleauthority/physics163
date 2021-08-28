from vpython import *

from util.math.Convert import Convert
from util.math.Unit import Unit
from physics.ElectricCharge import ElectricCharge
from physics.ElectricForce import ElectricForce

# Configure the scene
scene.width = 800
scene.height = 600
global_arrow_scale_factor = 3


class CoulombsLawSimulation:
    # Simulation configuration settings
    paused = False  # whether or not the sim is paused
    trace_log = False  # whether or not we are logging trace messages (such as values of r13, r23, f13, f23, etc.)
    x_step = 0.3e-11  # how much to step the loop per iteration

    # Physical constants in use for the simulation
    D = Convert.to_base(1, original_unit=Unit.NANO)  # distance of each statically positioned charge from origin
    E = 1.602e-19  # e; magnitude of electron charge
    X_MIN = -4 * D  # x min position
    X_MAX = 6 * D  # x max position

    def __init__(self):
        """Sets up the scene for the simulation"""
        # Set simulation x at X_MIN
        self.x = self.X_MIN

        # Create q1, a statically positioned charge located at D i-hat
        self.charge1 = ElectricCharge(value=-1 * self.E, position=vec(self.D, 0, 0), name="q1", value_alias="-e", draw=True,
                                      object_props=dict(radius=0.20 * self.D, color=color.cyan))

        # Create q2, a statically positioned charge located at -D i-hat
        self.charge2 = ElectricCharge(value=2 * self.E, position=vec(-self.D, 0, 0), name="q2", value_alias="2e", draw=True,
                                      object_props=dict(radius=0.24 * self.D, color=color.red))

        # Create q3, a dynamically positioned charge
        self.charge3 = ElectricCharge(value=-1 * self.E, position=vec(self.x, 0, 0), name="q3", value_alias="e", draw=True,
                                      object_props=dict(radius=0.15 * self.D, color=vec(0.8, 0, 1),
                                                        opacity=0.8))

        # The camera should follow q3
        scene.camera.follow(self.charge3.object)

        # Create and draw force13, the force of q1 on q3
        self.force13 = ElectricForce(q1=self.charge1, q2=self.charge3, draw=True,
                                     base_scale_factor=global_arrow_scale_factor, trace_log=self.trace_log,
                                     indicator_props=dict(color=self.charge1.object_props['color'], opacity=0.5))

        # Create and draw force23, the force of q2 on q3
        self.force23 = ElectricForce(q1=self.charge2, q2=self.charge3, draw=True,
                                     base_scale_factor=global_arrow_scale_factor, trace_log=self.trace_log,
                                     indicator_props=dict(color=self.charge2.object_props['color'], opacity=0.5))

        # Calculate the initial net force magnitude
        self.net_force = self.force13.value + self.force23.value
        self.net_force_mag = mag(self.net_force)

        # Create the initial graph objects
        self.x_net_force_graph = None
        self.x_net_force_curve = None
        self.create_graph()

        # Create UI buttons
        self.pause_button = button(bind=self.pause_sim, text="Pause")
        self.unpause_button = button(bind=self.unpause_sim, text="Unpause")
        self.reset_sim_button = button(bind=self.reset_sim, text="Reset")
        self.toggle_trace = checkbox(bind=self.toggle_trace,
                                     text="<abbr title='This will dump a lot of messages in the console. You've been warned.'>Trace Log</a>")

        # Some labels
        self.charge3_additional_label_tmpl = "x = {0:.3}nm"
        self.charge3_additional_label = label(pos=self.charge3.object.position + vec(0, 2e-9, 0),
                                              text="label not initialized")

    def toggle_trace(self):
        trace_log = not self.trace_log

        for item in (self, self.force13, self.force23):
            item.trace_log = trace_log

        print("Logging has been {0}".format("enabled" if self.trace_log else "disabled"))

    def pause_sim(self):
        if not self.paused:
            self.paused = True

            self.pause_button.disabled = True
            self.unpause_button.disabled = False
            self.reset_sim_button.disabled = False

            print("Simulation paused.")

    def unpause_sim(self):
        if self.paused:
            self.paused = False

            self.pause_button.disabled = False
            self.unpause_button.disabled = True
            self.reset_sim_button.disabled = True

            print("Simulation unpaused.")

            self.start_sim(start_x=self.x)

    def reset_sim(self):
        if not self.paused:
            # Can't reset the sim while it is running
            return

        self.x = self.X_MIN
        self.create_graph()

        print("Simulation reset.")

    def create_graph(self):
        if self.x_net_force_graph is not None:
            self.x_net_force_graph.delete()

        # Create and draw a graph plotting x in nanometers vs net force magnitude in piconewtons
        self.x_net_force_graph = graph(width=800, height=225, xmin=-4, xmax=6, ymin=-6000, ymax=6000,
                                       title="<b><i>x</i> (nm) vs <i>F<sub>net mag</sub></i> (pN)</b>",
                                       xtitle="<i>x</i> (nm)", ytitle="<i>F<sub>net mag</sub></i> (pN)",
                                       foreground=vec(0, 0, 0), background=vec(1, 1, 1))

        # Create a curve for plotting on the graph
        self.x_net_force_curve = gcurve(color=vec(0, 0.4, 1))

    def start_sim(self, start_x=X_MIN):
        x = start_x

        print("Simulation will begin at x = {0:.2e}m".format(x))

        while True and not self.paused:
            # This loop will run at a maximum of 90 its/sec
            rate(90)

            print("INFO: Starting iteration for x = {0:.2e}m".format(x)) if self.trace_log else None

            # Tick q3's new position
            q3_pos = vec(x, 0, 0)
            self.charge3.tick_obj_pos(q3_pos)
            self.force13.set_q2_pos(q3_pos)
            self.force23.set_q2_pos(q3_pos)

            # Tick q3 additional label
            self.charge3_additional_label.pos.x = x
            self.charge3_additional_label.text = self.charge3_additional_label_tmpl.format(
                Convert.to_nano(x, Unit.BASE))

            # Tick the forces
            self.force13.tick()
            self.force23.tick()

            # Recalculate the net force
            self.net_force = self.force13.value + self.force23.value
            self.net_force_mag = mag(self.net_force)

            # Add datapoint to the plot
            self.x_net_force_curve.plot(Convert.to_nano(x), Convert.to_pico(self.net_force.x))

            # Check if we've reached force equilibrium, allowing for small error margin
            if 0 < self.net_force_mag * 1e9 <= 0.00001:
                self.force13.scale_indicator(scale_factor=2e3)
                self.force23.scale_indicator(scale_factor=2e3)

                self.charge3_additional_label.text = "Charge 3 has reached force equilibrium\n" + self.charge3_additional_label_tmpl.format(
                    Convert.to_nano(x, Unit.BASE))

                print("Dynamic charge has reached force equilibrium. Arrow sizes have been adjusted larger.")

                break

            x += self.x_step

            if x >= self.X_MAX:
                break

        self.x = x
        print("Simulation loop has ended (either finished or paused) at x = {0:.2e}m".format(self.x))


# Start the simulation
sim = CoulombsLawSimulation()
sim.start_sim()
