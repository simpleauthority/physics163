from vpython import graph, gcurve, vec, rate
from helper.LogLevel import LogLevel


class Simulation:
    def __init__(self, auto_run: bool = False, paused: bool = False, log_level: LogLevel = LogLevel.ESSENTIAL):
        # Storage space specifically for graphs shown on screen
        self.graphs = self.create_graphs()

        # Storage space for various simulation data including physical objects
        self.sim_data = {
            "physical_objects": {}
        }

        # Configuration for the simulation
        self.config = {
            'auto_run': auto_run,
            'paused': paused,
            'log_level': log_level
        }

        if auto_run:
            self.run_simulation()

    def run_simulation(self):
        """Run the entire simulation"""
        self.log('Setting initial simulation data...', LogLevel.EVERYTHING)
        for (key, value) in self.create_sim_data():
            self.set_sim_data(key, value)

        self.log('Creating objects...', LogLevel.EVERYTHING)
        for (key, value) in self.create_objects():
            self.__add_object__(key, value)

        self.log('Creating graphs...', LogLevel.EVERYTHING)
        for item in self.create_graphs():
            self.__create_graph__(**item)

        self.log('Starting simulation loop...', LogLevel.EVERYTHING)
        self.run_simulation_loop()

    ##############################
    # Simulation data
    ##############################
    def create_sim_data(self):
        """Create arbitrary simulation data by returning a dict of data to store"""
        raise NotImplementedError("The create_sim_data method is not implemented.")

    def get_sim_data(self, name):
        """Gets a value out of the simulation data dictionary"""
        return self.sim_data.get(name)

    def set_sim_data(self, name, value):
        """Sets an arbitrary value in the simulation data dictionary"""
        self.sim_data[name] = value

    def incr_sim_data(self, name, amount=1):
        """Increments a numeric value in the sim data"""
        current = self.get_sim_data(name)

        if current is None:
            raise Exception("Sim data by that name does not exist")

        # noinspection PyTypeChecker
        self.set_sim_data(name, current + amount)

    def scale_by_sim_data(self, target, factor):
        scale_factor = self.get_sim_data(factor)

        return target * scale_factor

    ##############################
    # Physical objects
    ##############################
    def create_objects(self):
        """Return a dict of physical objects that should be in the simulation"""
        raise NotImplementedError("The create_objects method is not implemented.")

    def __add_object__(self, name, value):
        """Add a physical object into the simulation"""

        self.sim_data['physical_objects'][name] = value

    ##############################
    # Graphs
    ##############################
    def create_graphs(self):
        """Create the graphs by returning a list of dicts containing graph kwargs as needed"""
        raise NotImplementedError("The create graphs method is not implemented")

    def reset_graphs(self):
        """Reset the graphs in the simulation"""
        self.log('Simulation graphs will be deleted and recreated...', LogLevel.EVERYTHING)

        graphs = self.graphs.copy()

        for item in self.graphs:
            item.graph.delete()

        self.graphs.clear()

        for item in graphs:
            self.__create_graph__(to_recreate=item)

    def plot(self, graph_name, x, y):
        """Plot a value on a graph by name"""
        self.log('Plotting ({0},{1}) on graph {2}'.format(x, y, graph_name))

        found = self.__find_graph_by_name__(graph_name)

        if found is None:
            raise Exception("Graph by that name does not exist")

        found.c.plot(x, y)

    def __create_graph__(self, **kwargs):
        """Create a single graph and store it in the graph store"""
        name = kwargs.get('name', None)
        if name is None:
            raise Exception("Cannot have nameless graph")

        if self.__find_graph_by_name__(name) is not None:
            raise Exception("Graph by that name already exists.")

        to_recreate = kwargs.get('to_recreate', None)
        if to_recreate is not None:
            self.graphs.append(to_recreate)
        else:
            self.graphs.append(dict(
                name=name,
                graph=graph(title=kwargs.get('title', "No title"), xtitle=kwargs.get('x_title', "No x title"),
                            ytitle=kwargs.get('y_title', "No y title"), width=kwargs.get('width', 800),
                            height=kwargs.get('height', 240), xmin=kwargs.get('x_min', -10),
                            xmax=kwargs.get('x_max', 10), ymin=kwargs.get('y_min', -10), ymax=kwargs.get('y_max', 10),
                            foreground=kwargs.get('fg', vec(0, 0, 0)), background=kwargs.get('bg', vec(1, 1, 1))),
                curve=gcurve(color=kwargs.get('cfg', vec(0, 0, 0)))
            ))

    def __find_graph_by_name__(self, name):
        """Finds a graph by the earlier created name"""
        return next(filter(lambda obj: obj.name is name, self.graphs), None)

    ##############################
    # Simulation tick and loop
    ##############################
    def run_simulation_loop(self, itr_rate_lim=60):
        """
        This method handles the simulation loop. Should not need to be overwritten.
        """
        self.log("Running simulation loop", LogLevel.EVERYTHING)

        while self.simulation_sentinel() is True:
            self.log("Dumping simulation data for iteration: {0}".format(self.sim_data), LogLevel.EVERYTHING)

            rate(itr_rate_lim)

            if self.tick_simulation() is False:
                self.log("The simulation tick method returned False. There may be an error. Simulation ending.")
                break

    def simulation_sentinel(self):
        """Decides whether or not the loop should continue. Needs to return a bool."""
        raise NotImplementedError("The simulation loop sentinel is not implemented")

    def tick_simulation(self):
        """
        Run the code needed for a single tick (update) of the simulation.
        If this method returns False (not to replace simulation sentinel), the loop will exit.
        """
        raise NotImplementedError("The simulation tick method is not implemented")

    ##############################
    # Helpers and private methods
    ##############################
    def log(self, msg, level: LogLevel = LogLevel.ESSENTIAL):
        if self.check_config("log_level", level):
            print("> [{0}]: {1}".format(level, msg))

    def check_config(self, name, value):
        """Verifies that a particular config option has a particular value"""
        return self.__get_config__(name) is value

    def __get_config__(self, name):
        """Gets a configuration value from the config dict"""
        return self.config.get(name)

    def __set_config__(self, name, value):
        """Sets a configuration value into the config dict"""
        if self.__get_config__(name) is None:
            raise Exception("Config value by that name does not exist.")

        self.config[name] = value
