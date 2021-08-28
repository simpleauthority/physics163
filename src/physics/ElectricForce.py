from vpython import arrow, mag


class ElectricForce:
    """
    ElectricForce represents an electric force from one charge on to another charge. In this class's case, it represents
    the charge of q1 onto q2. The class makes use of Coulomb's Law to calculate this force. The class also accepts a
    dictionary of indicator properties to draw an automatically scaled arrow on q2 if desired.
    """
    K = 8.99e9  # Coulomb's constant

    def __init__(self, q1, q2, name, draw=True, base_scale_factor=1, trace_log=False, indicator_props=None):
        if indicator_props is None:
            indicator_props = {}

        self.q1 = q1
        self.q2 = q2
        self.name = name
        self.base_scale_factor = base_scale_factor
        self.trace_log = trace_log
        self.indicator_props = indicator_props
        self.indicator = None
        self.tick()

        if bool(draw):
            self.draw_indicator()

    def set_q1_pos(self, pos):
        """Tick the position of q1"""
        self.q1.position = pos

    def set_q2_pos(self, pos):
        """Tick the position of q2"""
        self.q2.position = pos

    def __tick_r_vec__(self):
        """Calculate the r-vector.py from q1 to q2"""
        self.r_vector = self.q2.position - self.q1.position
        # if self.trace_log:
        #     print("INFO: New r-vector.py for force of {0} on {1} calculated as {2}".format(self.q1.get_label_text(),
        #                                                                                 self.q2.get_label_text(),
        #                                                                                 self.r_vector))
        return self.r_vector

    def __tick_force__(self):
        """Calculate electric force between q1 and q2"""
        self.value = (self.K * self.q1.value * self.q2.value * self.r_vector) / (mag(self.r_vector) ** 3)
        # if self.trace_log:
        #     print("INFO: New value for force of {0} on {1} calculated as {2}".format(self.q1.get_label_text(),
        #                                                                              self.q2.get_label_text(),
        #                                                                              self.value))
        return self.value

    def draw_indicator(self):
        """Draw the indicator arrow at q2.pos"""
        if self.indicator is None:
            self.indicator = arrow(pos=self.q2.position, axis=self.value * self.indicator_scale_factor(
                base_scale_factor=self.base_scale_factor), **self.indicator_props)

    def tick_indicator(self):
        """Tick the indicator position and axis"""
        if self.indicator is not None:
            self.indicator.position = self.q2.position
            self.indicator.axis = self.value * self.indicator_scale_factor(base_scale_factor=self.base_scale_factor)

    def tick(self):
        """Tick the force (recalculate r-vector.py and force)"""
        self.__tick_r_vec__()
        self.__tick_force__()
        self.tick_indicator()

    def print(self):
        print("force {0} = ".format(self.name), self.value)
        print("force mag {0} = ".format(self.name), mag(self.value))

    def indicator_scale_factor(self, size_lower_bound=10, size_upper_bound=100, base_scale_factor=1):
        """
        Inspect the force magnitude and decide on either 1) a proportional scale factor
        or 2) the constant scale factor
        """

        force_mag = mag(self.value)

        if force_mag < size_lower_bound:
            # We need to make the indicator bigger
            if self.trace_log:
                print("INFO: Force mag is {0} < {1} so indicator scale will be adjusted larger".format(force_mag,
                                                                                                       size_lower_bound))
            return base_scale_factor
        elif size_lower_bound <= force_mag <= size_upper_bound:
            # No need to rescale the arrow at this time
            # if self.trace_log:
            # print("INFO: Force mag is {0}N <= {1} <= {2} so indicator scale will not be adjusted".format(size_lower_bound, force_mag,vsize_upper_bound))
            return base_scale_factor
        else:
            # We need to make the indicator smaller
            if self.trace_log:
                print("INFO: Force mag is {0} > {1} so indicator scale will be adjusted smaller".format(force_mag,
                                                                                                        size_upper_bound))
            return base_scale_factor * 1e-7

    def scale_indicator(self, scale_factor=None):
        """Scale the indicator by the given value"""
        if scale_factor is None:
            # reset axis if scale_factor not provided
            # print("INFO: Resetting indicator scale to force value") if self.trace_log else None
            self.indicator.axis = self.value
        else:
            # multiply axis by provided scale_factor
            # print("INFO: Scaling indicator by scale factor of {0:.2e}".format(scale_factor)) if self.trace_log else None
            self.indicator.axis *= scale_factor
